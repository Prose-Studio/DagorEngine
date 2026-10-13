# DEP_DOMAIN prog/tools
"""csq.exe builds of a revision, out of the source tree, in several code layouts.

The build replays the commands of the Rel build of csq in the engine's windows-cdk
tree (build/windows-cdk). It compiles only the objects that include the Quirrel
headers, from a copy of the Quirrel sources of the revision; all other code links
from the output of that tree. A build of the sources that the tree built has the
same .text as its csq.exe.

Variants of one revision, in WORK/<label>/<variant>/csq.exe (+ csq.pdb):
  nat     the plain build, as the tree makes it
  k<K>    SQVM::Execute aligned to 64 bytes, and K NOP bytes after its prologue
"""
import collections
import concurrent.futures as cf
import functools
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, *[".."] * 6))
BUILD_DIR = os.path.normpath(os.environ.get("VMPERF_BUILD") or os.path.join(REPO, "build", "windows-cdk"))
BUILD_CMD = "cmake --build --preset windows-cdk --config Rel --target csq"  # in prog/
WORK = os.environ.get("VMPERF_WORK") or os.path.join(REPO, "build", "quirrel-vmperf")
QUIRREL = "prog/1stPartyLibs/quirrel/quirrel"
SRC_DIRS = [QUIRREL, "prog/gameLibs/quirrel/quirrelHost"]
NOT_COMPILED = [f"{QUIRREL}/{d}" for d in ("bench", "doc", "testData", "sq_llvm_fuzzer")]
LAYOUTS = ["k0", "k16", "k32", "k48"]
VARIANTS = ["nat"] + LAYOUTS
WORKTREE = "wt"
# the clang-cl options that name the Windows SDK and the MSVC tools (their value is the next argument)
SDK_OPTIONS = ("/vctoolsdir", "/winsdkdir", "/winsdkversion")

# the Rel build of csq: compiles {obj: command line} (of the whole tree, compile_args() splits one), libs {lib: argv}
# (those of the link), the csq.exe link argv; the keys are absolute and normalized (norm()), the commands keep the
# tree's relative paths and run in its dir
Build = collections.namedtuple("Build", "compiles libs link")


def split_args(line):
    """The arguments of a Windows command line, as CommandLineToArgvW splits it."""
    args, arg, quoted, i, have = [], [], False, 0, False
    while i < len(line):
        c = line[i]
        if c == "\\":
            n = len(line) - i - len(line[i:].lstrip("\\"))
            if i + n < len(line) and line[i + n] == '"':
                arg.append("\\" * (n // 2))
                if n % 2:
                    arg.append('"')
                    i += n + 1
                else:
                    i += n
            else:
                arg.append("\\" * n)
                i += n
            have = True
            continue
        if c == '"':
            quoted, have = not quoted, True
        elif c in " \t" and not quoted:
            if have:
                args.append("".join(arg))
                arg, have = [], False
        else:
            arg.append(c)
            have = True
        i += 1
    if have:
        args.append("".join(arg))
    return args


def tool_command(command):
    """The command of a rule that cmd.exe runs (cmd.exe /C "cd . && <command> && ..."), split."""
    m = re.match(r'^\S*cmd\.exe /C "cd \. && (.*)"$', command, re.I)
    return split_args(m.group(1).split(" && ")[0] if m else command)


def norm(path):
    return os.path.normpath(os.path.join(BUILD_DIR, path)).replace("\\", "/").lower()


@functools.cache
def cdk_build():
    """The commands of the Rel build of csq in the windows-cdk tree (from its build-Rel.ninja)."""
    try:
        with open(os.path.join(BUILD_DIR, "CMakeCache.txt")) as f:
            ninja = re.search(r"^CMAKE_MAKE_PROGRAM:\w+=(.*)$", f.read(), re.M).group(1)
    except (OSError, AttributeError):
        raise SystemExit(f"{BUILD_DIR} is not a configured windows-cdk tree; run {BUILD_CMD} in prog/") from None
    proc = subprocess.run([ninja, "-C", BUILD_DIR, "-f", "build-Rel.ninja", "-t", "compdb", "-x"],
                          capture_output=True, text=True, errors="replace")
    if proc.returncode:
        raise SystemExit(f"ninja failed in {BUILD_DIR}:\n{proc.stdout[-3000:]}\n{proc.stderr}")
    compiles, libs, link = {}, {}, None
    for edge in json.loads(proc.stdout):
        output = norm(edge.get("output", ""))
        command = edge["command"]
        if output.endswith(".obj") and "clang-cl.exe" in command[:300].lower():
            compiles[output] = command
        elif output.endswith(".lib") and "llvm-lib.exe" in command.lower():
            libs[output] = tool_command(command)
        elif output.endswith("/bin/csq.exe"):
            cmd = tool_command(command)
            link = cmd[cmd.index("--") + 1:] if "--" in cmd else cmd  # the linker of cmake -E vs_link_exe
    if link is None or not libs:
        raise SystemExit(f"no Rel commands for csq.exe in {BUILD_DIR}; run {BUILD_CMD} in prog/")
    linked = {norm(a) for a in link}
    return Build(compiles, {lib: cmd for lib, cmd in libs.items() if lib in linked}, link)


def lib_members(build, lib):
    return [a for a in build.libs[lib][1:] if a.lower().endswith(".obj")]


@functools.cache
def compile_args(obj):
    """The arguments of the compile of obj (of the tree), from clang-cl (without a compiler launcher, sccache)."""
    cmd = split_args(cdk_build().compiles[obj])
    return next(cmd[i:] for i, a in enumerate(cmd) if a.lower().endswith("clang-cl.exe"))


@functools.cache
def llvm_bin():
    """The LLVM bin directory of the toolchain of the tree."""
    return os.path.dirname(compile_args(next(iter(cdk_build().compiles)))[0])


def sdk_args():
    """The compiler's and the linker's arguments that find the Windows SDK and the MSVC libraries."""
    build = cdk_build()
    cmd = compile_args(next(iter(build.compiles)))
    sdk_compile = [a for i, a in enumerate(cmd) if a in SDK_OPTIONS or cmd[i - 1] in SDK_OPTIONS]
    sdk_link = [a for a in build.link if a.lower().startswith(tuple(f"{o}:" for o in SDK_OPTIONS) + ("/libpath:",))]
    return sdk_compile, sdk_link


@functools.cache
def label_of(rev):
    if rev == WORKTREE:
        return WORKTREE
    try:
        return git("rev-parse", "--short=12", rev + "^{commit}").strip()
    except subprocess.CalledProcessError:
        raise SystemExit(f"{rev} is neither a git revision, nor `{WORKTREE}`, nor a file") from None


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, text=True, check=True).stdout


def exe_path(label, variant):
    return os.path.join(WORK, label, variant, "csq.exe")


def sqvm_source(label):
    return os.path.join(WORK, label, "sqvm.cpp")


PATHSPEC = ["--"] + SRC_DIRS + [f":(exclude){d}" for d in NOT_COMPILED]
# the source dirs in the arguments of the commands (any separator, any case)
SRC_DIRS_RE = re.compile("|".join(r"[\\/]".join(map(re.escape, re.split(r"[\\/]", f"{REPO}/{d}"))) for d in SRC_DIRS),
                         re.I)


def worktree_files():
    files = git("ls-files", "-co", "--exclude-standard", *PATHSPEC).splitlines()
    return [rel for rel in files if os.path.isfile(os.path.join(REPO, rel))]


def stamp_of(rev):
    """What a build of rev is made from: the commit, or a digest of the working tree files."""
    if rev != WORKTREE:
        return label_of(rev)
    digest = hashlib.sha1()
    for rel in worktree_files():
        digest.update(rel.encode())
        with open(os.path.join(REPO, rel), "rb") as f:
            digest.update(f.read())
    return "worktree " + digest.hexdigest()


def link_inputs(build):
    """The files that the link takes from the tree, as they are: not rebuilt, not with rebuilt objects."""
    files = []
    for a in build.link[1:]:
        if norm(a) in build.libs:
            members = lib_members(build, norm(a))
            if any(uses_quirrel(build.compiles.get(norm(o))) for o in members):
                files += [o for o in members if not uses_quirrel(build.compiles.get(norm(o)))]
            else:
                files.append(a)
        elif a.lower().endswith(".obj") and not uses_quirrel(build.compiles.get(norm(a))):
            files.append(a)
    return files


def inputs_stamp(build):
    """A digest of the files that the link takes from the tree, so that a build is made again when the tree rebuilt
    any of them."""
    digest = hashlib.sha1()
    for f in link_inputs(build):
        try:
            st = os.stat(os.path.join(BUILD_DIR, f))
        except FileNotFoundError:
            raise SystemExit(f"{f} is missing in {BUILD_DIR}; run {BUILD_CMD} in prog/") from None
        digest.update(f"{f} {st.st_size} {st.st_mtime_ns}\n".encode())
    return digest.hexdigest()


def mirror(rev, dst):
    if rev == WORKTREE:
        for rel in worktree_files():
            os.makedirs(os.path.dirname(os.path.join(dst, rel)), exist_ok=True)
            shutil.copy2(os.path.join(REPO, rel), os.path.join(dst, rel))
    else:
        data = subprocess.run(["git", "-C", REPO, "archive", rev] + PATHSPEC, capture_output=True, check=True).stdout
        with tarfile.open(fileobj=io.BytesIO(data)) as tar:
            tar.extractall(dst, filter="data")


def in_copy(arg, src_root):
    """arg with the source dirs of the repo replaced by those of the copy in src_root."""
    return SRC_DIRS_RE.sub(lambda m: src_root + m.group(0)[len(REPO):], arg)


def compile_cmd(cmd, src_root, obj, source=None):
    # same __FILE__ strings as the tree's build: the copy maps to the repo as the command spells it
    repo = next(m.group(0)[:len(REPO)] for m in map(SRC_DIRS_RE.search, reversed(cmd)) if m)
    res = [cmd[0], f"/clang:-ffile-prefix-map={src_root}={repo}"]
    for a in cmd[1:]:
        if a.startswith(("-clang:-MD", "-clang:-MT", "-clang:-MF", "/showIncludes", "-showIncludes")):  # its depfiles
            continue
        if a.startswith("/Fo"):
            a = "/Fo" + obj
        elif a.startswith("/Fd"):
            a = "/Fd" + os.path.join(os.path.dirname(obj), "objs.pdb")
        else:
            a = in_copy(a, src_root)
        res.append(a)
    if source:
        res[-1] = source
    return res


def uses_quirrel(command):
    return command is not None and SRC_DIRS_RE.search(command) is not None


def run_all(jobs):
    def run(job):
        return job[0], subprocess.run(job[1], cwd=BUILD_DIR, capture_output=True, text=True)

    with cf.ThreadPoolExecutor(max_workers=os.cpu_count() or 8) as ex:
        failed = [(name, r.stdout + r.stderr) for name, r in ex.map(run, jobs) if r.returncode]
    if failed:
        raise SystemExit("\n".join(f"FAILED {name}\n{out}" for name, out in failed))


def layout_source(text, k, file_name):
    """sqvm.cpp with Execute aligned to 64 and K NOP bytes at the start of its body; the
    #line directives keep the file name and line numbers of the original."""
    m = re.search(r"^template <bool debughookPresent>\r?\n(bool SQVM::Execute\(.*\)\r?\n\{\r?\n)", text, re.M)
    if not m:
        raise SystemExit("the definition of SQVM::Execute in sqvm.cpp is not where build.py expects it")
    line = text.count("\n", 0, m.end()) + 1
    pad = f'__asm__ volatile(".skip {k}, 0x90");\n' if k else ""
    name = file_name.replace("\\", "\\\\")
    return (f'#line 1 "{name}"\n' + text[:m.start(1)] + "__attribute__((aligned(64))) " + m.group(1) + pad
            + f'#line {line} "{name}"\n' + text[m.end():])


def rel_dir(path):
    """The path of a file of the tree, relative to its dir."""
    return os.path.relpath(path, BUILD_DIR.replace("\\", "/").lower())


def link(build, objs, out_dir):
    """Link csq.exe into out_dir, objs {obj of the tree: obj to use instead}."""
    os.makedirs(out_dir, exist_ok=True)
    inputs = dict(objs)
    for lib, cmd in build.libs.items():
        members = lib_members(build, lib)
        if any(norm(o) in objs for o in members):
            out_lib = os.path.join(out_dir, "lib", rel_dir(lib))
            os.makedirs(os.path.dirname(out_lib), exist_ok=True)
            with open(out_lib + ".rsp", "w") as f:
                f.write("\n".join(f'"{objs.get(norm(o), o)}"' for o in members))
            subprocess.run([cmd[0], "/nologo", "/out:" + out_lib, "@" + out_lib + ".rsp"], cwd=BUILD_DIR, check=True)
            inputs[lib] = out_lib
    argv = []
    for a in build.link[1:]:
        low = a.lower()
        if low.startswith("/out:"):
            a = "/out:" + os.path.join(out_dir, "csq.exe")
        elif low.startswith("/implib:"):
            a = "/implib:" + os.path.join(out_dir, "csq.lib")
        elif low.startswith("/pdb:"):
            argv.append("/pdbaltpath:" + os.path.join(BUILD_DIR, a[5:]))  # the same embedded path as the tree's build
            a = "/pdb:" + os.path.join(out_dir, "csq.pdb")
        elif low.endswith((".obj", ".lib")):
            a = inputs.get(norm(a), a)
        argv.append(a)
    rsp = os.path.join(out_dir, "link.rsp")
    with open(rsp, "w") as f:
        f.write("\n".join(f'"{a}"' if " " in a else a for a in argv))
    subprocess.run([build.link[0], "@" + rsp], cwd=BUILD_DIR, check=True)
    shutil.rmtree(os.path.join(out_dir, "lib"), ignore_errors=True)


def build(rev, rebuild=False):
    """Build all variants of rev (a git revision or WORKTREE) and return its label. A build
    is used again while its sources and the output of the tree that it links stay the same."""
    label = label_of(rev)
    root = os.path.join(WORK, label)
    tree = cdk_build()
    stamp, stamp_file = f"{stamp_of(rev)}, tree output {inputs_stamp(tree)}", os.path.join(root, "stamp.txt")
    if not rebuild and os.path.exists(stamp_file) and all(os.path.exists(exe_path(label, v)) for v in VARIANTS):
        with open(stamp_file) as f:
            if f.read().strip() == stamp:
                return label
    print(f"building {rev} -> {root}", flush=True)
    if os.path.exists(root):
        shutil.rmtree(root)
    src_root = os.path.normpath(os.path.join(root, "src"))
    mirror(rev, src_root)

    used = {norm(o) for lib in tree.libs for o in lib_members(tree, lib)}  # the objects of the link
    used |= {norm(a) for a in tree.link if a.lower().endswith(".obj")}
    objs = {o: os.path.join(root, "obj", rel_dir(o)) for o in sorted(used) if uses_quirrel(tree.compiles.get(o))}
    for obj in objs.values():
        os.makedirs(os.path.dirname(obj), exist_ok=True)
    run_all([(compile_args(o)[-1], compile_cmd(compile_args(o), src_root, obj)) for o, obj in objs.items()])
    link(tree, objs, os.path.join(root, "nat"))

    sqvm = [o for o in objs if norm(compile_args(o)[-1]).endswith("/squirrel/sqvm.cpp")]
    if len(sqvm) != 1:
        raise SystemExit(f"expected one sqvm.cpp object, found {sqvm}")
    sqvm = sqvm[0]
    file_name = compile_args(sqvm)[-1]
    original = in_copy(file_name, src_root)
    with open(original, encoding="utf-8", newline="") as f:
        text = f.read()
    shutil.copy(original, sqvm_source(label))  # for the profile report
    jobs = []
    for variant in LAYOUTS:
        out_dir = os.path.join(root, variant)
        os.makedirs(out_dir, exist_ok=True)
        # next to the original, for its quoted includes
        source = original[:-len(".cpp")] + f"_{variant}.cpp"
        with open(source, "w", encoding="utf-8", newline="") as f:
            f.write(layout_source(text, int(variant[1:]), file_name))
        jobs.append((source, compile_cmd(compile_args(sqvm), src_root, os.path.join(out_dir, "sqvm.obj"), source)))
    run_all(jobs)
    for variant in LAYOUTS:
        link(tree, {**objs, sqvm: os.path.join(root, variant, "sqvm.obj")}, os.path.join(root, variant))
    shutil.rmtree(os.path.join(root, "obj"))
    shutil.rmtree(os.path.join(root, "src"))
    with open(stamp_file, "w") as f:
        f.write(stamp + "\n")
    return label
