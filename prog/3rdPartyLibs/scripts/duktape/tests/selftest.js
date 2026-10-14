// The checks of the duktape interpreter (the CDK's command line ECMAScript engine): numbers, strings, regular
// expressions, JSON, arrays, objects and closures, exceptions, dates, the ES2015 parts Duktape 2.2 has, its own
// builtins and the command line's extras (print, console, require, readFile/writeFile). Any failed check throws at the
// end, so the interpreter exits with 1; it runs in its working dir (selftest.tmp is written there).
var failures = [];
var checks = 0;

function check(name, actual, expected) {
  checks++;
  var same = (typeof expected === 'number' && isNaN(expected)) ? (typeof actual === 'number' && isNaN(actual))
                                                                : actual === expected;
  if (!same)
    failures.push(name + ': ' + Duktape.enc('jx', actual) + ', expected ' + Duktape.enc('jx', expected));
}

function throwsType(name, fn, type) {
  checks++;
  try {
    fn();
    failures.push(name + ': did not throw');
  } catch (e) {
    if (!(e instanceof type))
      failures.push(name + ': threw ' + e.name + ', expected ' + type.name);
  }
}

// numbers
check('integer arithmetic', 7 * 6 - 4 / 2 + 10 % 4, 42);
check('2^53 is exact', Math.pow(2, 53) + 1 - Math.pow(2, 53), 0);
check('2^53 - 1 is exact', 9007199254740991 - 9007199254740990, 1);
check('binary fractions', 0.1 + 0.2 === 0.3, false);
check('rounding', (0.1 + 0.2).toFixed(2), '0.30');
check('shortest round trip', String(0.1 + 0.2), '0.30000000000000004');
check('exponent form', String(1e21), '1e+21');
check('bitwise', (0xF0 | 0x0F) ^ 0xFF, 0);
check('signed shift', -16 >> 2, -4);
check('unsigned shift', -1 >>> 28, 15);
check('radix', (255).toString(16) + (8).toString(2), 'ff1000');
check('parseInt', parseInt('0x1A', 16) + parseInt('077', 10), 103);
check('parseFloat', parseFloat('3.25e2px'), 325);
check('NaN', 0 / 0, NaN);
check('Infinity', 1 / 0 === Infinity && -1 / 0 === -Infinity, true);
check('negative zero', 1 / -0, -Infinity);
check('Math', Math.floor(Math.sqrt(2) * 1000) + Math.max(3, 9, 1) + Math.abs(-2), 1425);
check('Math.round halves up', [Math.round(2.5), Math.round(-2.5), Math.round(-2.6)].join(), '3,-2,-3');

// strings
check('length in UTF-16 units', 'ü日😀'.length, 4);
check('charCodeAt', 'Aé'.charCodeAt(1), 0xe9);
check('fromCharCode', String.fromCharCode(72, 105), 'Hi');
check('case', 'Straße'.toUpperCase() + 'ABC'.toLowerCase(), 'STRASSEabc');
check('trim', '  \t pad \n '.trim(), 'pad');
check('split and join', 'a,b,,c'.split(',').join('|'), 'a|b||c');
check('indexOf', 'hello world'.indexOf('o', 5) + 'hello'.lastIndexOf('l'), 10);
check('substring', 'engine'.substring(1, 4) + 'engine'.substr(-3), 'ngiine');
check('URI', encodeURIComponent('a b&é') + decodeURIComponent('%E2%9C%93'), 'a%20b%26%C3%A9✓');

// regular expressions
var m = /(\d{4})-(\d{2})-(\d{2})/.exec('date: 2026-10-14!');
check('regexp groups', m && m.slice(1).join('/'), '2026/10/14');
check('regexp global replace', 'a1b22c333'.replace(/\d+/g, function (d) { return '<' + d.length + '>'; }),
      'a<1>b<2>c<3>');
var re = /o/g;
re.exec('foo');
check('regexp lastIndex', re.lastIndex, 2);
check('regexp flags', /abc/i.test('xABCx') && !/^abc$/m.test('xabc'), true);

// JSON
var obj = {name: 'Grün "quoted"', list: [1, 2.5, null, true], nested: {empty: {}, arr: []}, n: -0.000125};
var text = JSON.stringify(obj);
check('JSON text', text, '{"name":"Grün \\"quoted\\"","list":[1,2.5,null,true],"nested":{"empty":{},"arr":[]},' +
      '"n":-0.000125}');
check('JSON round trip', JSON.stringify(JSON.parse(text)), text);
check('JSON indent', JSON.stringify({a: [1]}, null, 2), '{\n  "a": [\n    1\n  ]\n}');
check('JSON reviver', JSON.parse('{"a":1,"b":2}', function (k, v) { return k === 'a' ? v * 10 : v; }).a, 10);
check('JSON escapes', JSON.parse('"\\u0041\\n\\t"'), 'A\n\t');
throwsType('JSON syntax error', function () { JSON.parse('{"a":}'); }, SyntaxError);

// arrays, objects, closures
var nums = [5, 3, 10, 1];
check('sort numeric', nums.slice().sort(function (a, b) { return a - b; }).join(), '1,3,5,10');
check('sort default', nums.slice().sort().join(), '1,10,3,5');
check('map filter reduce', nums.map(function (x) { return x * 2; }).filter(function (x) { return x > 5; })
  .reduce(function (s, x) { return s + x; }, 0), 36);
var spliced = [1, 2, 3, 4];
check('splice', spliced.splice(1, 2, 'x').join() + '|' + spliced.join(), '2,3|1,x,4');
check('isArray', Array.isArray([]) && !Array.isArray({length: 0}), true);
check('key order', Object.keys({b: 1, a: 2, 1: 3, 0: 4}).join(), '0,1,b,a');
var counter = (function () { var n = 0; return function () { return ++n; }; })();
counter();
check('closure', counter(), 2);
var proto = {greet: function () { return 'hi ' + this.name; }};
var child = Object.create(proto);
child.name = 'duk';
check('prototype', child.greet() + (Object.getPrototypeOf(child) === proto), 'hi duktrue');
var accessor = {};
Object.defineProperty(accessor, 'twice', {get: function () { return 21 * 2; }, enumerable: false});
check('getter', accessor.twice + Object.keys(accessor).length, 42);
check('bind', (function (a, b) { return this.x + a + b; }).bind({x: 1}, 2)(3), 6);
check('arguments', (function () { return arguments.length; })(1, 2, 3), 3);

// exceptions
var order = [];
try {
  try {
    order.push('try');
    null.property;
  } finally {
    order.push('finally');
  }
} catch (e) {
  order.push(e instanceof TypeError ? 'TypeError' : e.name);
}
check('try finally catch', order.join(), 'try,finally,TypeError');
throwsType('ReferenceError', function () { return undefinedVariable; }, ReferenceError);
throwsType('RangeError', function () { return new Array(-1); }, RangeError);
var custom = new Error('boom');
check('Error', custom.message + (custom instanceof Error), 'boomtrue');

// dates (UTC only: the time zone of the machine must not matter)
var date = new Date(Date.UTC(2020, 1, 29, 12, 30, 15, 250));
check('Date ISO', date.toISOString(), '2020-02-29T12:30:15.250Z');
check('Date parse', Date.parse('2020-02-29T12:30:15.250Z'), date.getTime());
check('Date fields', date.getUTCDay() + date.getUTCMonth() * 10, 16);

// ES2015 parts
var u8 = new Uint8Array([1, 2, 255]);
check('Uint8Array', u8.length + u8[2], 258);
var view = new DataView(new ArrayBuffer(4));
view.setUint16(0, 0x1234, true);
check('DataView little endian', new Uint8Array(view.buffer)[0], 0x34);
var trapped = new Proxy({}, {get: function (t, k) { return 'got ' + k; }});
check('Proxy', trapped.anything, 'got anything');
check('Reflect', Reflect.has({a: 1}, 'a') && !Reflect.has({}, 'a'), true);
check('Object.setPrototypeOf', Object.getPrototypeOf(Object.setPrototypeOf({}, proto)) === proto, true);

// Duktape's builtins
check('Duktape.version', Duktape.version >= 20200, true);
check('hex', Duktape.enc('hex', 'Duk'), '44756b');
check('base64', Duktape.enc('base64', 'Duktape'), 'RHVrdGFwZQ==');
check('base64 decode', String.fromBufferRaw(Duktape.dec('base64', 'RHVrdGFwZQ==')), 'Duktape');
check('jx', Duktape.enc('jx', {u: undefined, f: function () {}, n: NaN}), '{u:undefined,f:{_func:true},n:NaN}');

// the command line's extras
check('print', typeof print, 'function');
check('console', typeof console.log, 'function');
Duktape.modSearch = function (id) {
  if (id === 'answer')
    return 'exports.value = 6 * 7;';
  throw new Error('module not found: ' + id);
};
check('require', require('answer').value, 42);
throwsType('require missing', function () { require('missing'); }, Error);
writeFile('selftest.tmp', Duktape.dec('hex', '00017f80ff0a0d')); // a plain buffer: written as is
check('binary file round trip', Duktape.enc('hex', readFile('selftest.tmp')), '00017f80ff0a0d');
writeFile('selftest.tmp', 'café'); // a string: written as UTF-8
check('text file round trip', Duktape.enc('hex', readFile('selftest.tmp')), '636166c3a9');
throwsType('readFile missing', function () { readFile('selftest.missing'); }, TypeError);

if (failures.length)
  throw new Error(failures.length + ' of ' + checks + ' checks failed:\n  ' + failures.join('\n  '));
print('duktape selftest: ' + checks + ' checks passed');
