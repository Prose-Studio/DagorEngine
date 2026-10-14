// An uncaught error must make the interpreter exit with 1: what lets selftest.js fail its test
throw new Error('this script fails on purpose');
