# The Dagor CMake build

How the engine and its projects build with CMake, and why. The reference of each function is the comment at the top of
its module; this file is the map and the decisions behind it.

## Layout

```
prog/CMakeLists.txt       the engine: project(DagorEngine), include(cmake/Dagor.cmake), the areas
prog/CMakePresets.json    the engine's trees (cmake --list-presets), on cmake/presets/base.json
prog/cmake/               Dagor.cmake (the entry), DagorConfig.cmake (find_package(Dagor)), the Dagor*.cmake modules,
                          platform/<CMAKE_SYSTEM_NAME>.cmake, toolchains/, presets/, find/ (SDKs), sdk/manifest.cmake,
                          scripts/, templates/
<project>/prog/CMakeLists.txt + CMakePresets.json   a game (templates/, dng.py new)
```

There is no CMakeLists.txt at the repository root: prog/ is the engine's top level. Build trees are
`build/<preset>` next to prog/ (of the engine or the project); only intermediates go there.

## Trees and presets

A tree is a preset: a target platform and compiler (the hidden `toolchain-*` bases of cmake/presets/base.json, each
with its toolchain file) and a variant, `DAGOR_VARIANT`, which sets the defaults of the options (DagorOptions.cmake).
The `<host>[-<compiler>|-<arch>]` presets (`windows`, `linux-clang`, ...) are a tree of their own that builds every tree
of that platform and compiler with its preset, one after the other (DagorAll.cmake, `DAGOR_ALL_PRESETS`):
`cmake --workflow --preset windows` on a fresh clone does what jam's devtools setup and full build did. A project's
`<host>` workflow likewise builds the client, its content and a multiplayer game's dedicated server.

| variant | builds by default |
|---|---|
| `tests` | the engine's unit tests (CTest; the `-ci` test presets skip those that need a GPU or a display) |
| `cdk` | the command-line tools of the content pipeline on the static kernel; `--install --component cdk` puts them in `tools/dagor_cdk/<platform>-<arch>` |
| `assets` | the asset build on daKernel (the shared kernel): daBuild with its exporter plugins, ddsxCvt2; the host tools of the games' content |
| `editor` | the GUI editors on daKernel: daEditor3x with its plugins, AssetViewer, impostorBaker, blkEditor, plodGen |
| `dargbox` | the daRg sandbox |
| `maxplug` | the 3ds Max plugin (with the Max SDK: `MaxSDK_ROOT`, `DAGOR_MAX_VERSION`; MSVC, the DLL CRT) |
| `game` | a project's game: its presets `<host>-client`, `<host>-dedicated`, `<host>-aot-compiler` |

Configurations are Dev (optimized, asserts and logs on), Rel, IRel (Rel with logs) and Dbg, in one Ninja Multi-Config
tree. Workflow presets chain configure, build and test (or package).

Variants are separate trees where jam built separate configurations that one tree cannot hold: the kernel linkage
(static in cdk and tests, daKernel in assets and editor), and the 3d driver interface, whose `_TARGET_D3D_MULTI` applies
to all the code of a tree: the assets tree's programs link the null driver directly, the editors' (and dargbox's) the
platform's drivers through the multi-driver interface. The editors are games on daNetGame (daEditor3x is `editor_dng`,
AssetViewer `asset_viewer_dng`, each with its list of daNetGameLibs) with the game features off and Jolt; the editor
tree builds daNetGame for them like a game tree. A tree's command-line tools that link the null driver are not in the
multi-driver trees.

## Targets

One CMakeLists.txt per module dir, one `dagor_add_target()` call per target in it (like O3DE's `ly_add_target`):

```cmake
dagor_add_target(NAME engine.math STATIC
  FILES_CMAKE math_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
)
```

- The sources are in `<name>_files.cmake` next to it (`FILES`, `ES_FILES`, `DAS_FILES`, `STRINGIFY_FILES`,
  `STRINGIFY_ARRAY_FILES`); `<name>_<platform>_files.cmake` adds a platform's (windows, linux, macos, ios, android;
  apple for both Apple platforms) and `<name>_<platform>.cmake` its settings. Adding or removing a source edits a
  `_files.cmake`; a CMakeLists.txt changes only when targets or dependencies do.
- The areas (prog/3rdPartyLibs, 1stPartyLibs, engine, commonFx, gameLibs, daNetGameLibs, tools) add every module dir
  themselves, by relative path, under the conditions it builds on. Module dirs add none, so no variable leaks from
  one module into another.
- Targets are named after their dir under prog/ with dots (`engine.math`); a few have `Dagor::` aliases for what
  projects link (Dagor::Quirrel, Dagor::Phys). `CMAKE_LINK_LIBRARIES_ONLY_TARGETS` is on: a misspelled dependency is
  a configure error. System libraries are `System::<name>` imported targets.
- Kinds: STATIC (default), OBJECT, SHARED, MODULE, HEADERONLY (an INTERFACE library), EXECUTABLE [APPLICATION]
  [MACOSX_BUNDLE]. The INTERFACE and WIN32 keywords are spelt HEADERONLY and APPLICATION because the scope INTERFACE and
  the define WIN32 are values of the other keywords.
- Kinds of target with more to them are functions with the same arguments: `dagor_add_catch2_test`,
  `dagor_add_dng_module`, `dagor_add_dng_game`, `dabuild_plugin`, `dsc2_compiler`. They append their own
  `FILES_CMAKE`/`BUILD_DEPENDENCIES` to the caller's (repeated multi-value keywords accumulate).
- Libraries are built for the programs that link them (EXCLUDE_FROM_ALL); the variant names its programs
  (`dagor_build_by_default`, prog/CMakeLists.txt); a project's programs are built by default.
- First-party code gets the strict warning set (errors with DAGOR_WARNINGS_AS_ERRORS); LAX gives third-party code the
  lax one. Settings of the whole tree are directory-level (add_compile_options & co. with generator expressions,
  DagorCompilerFlags.cmake and platform/), not per-target boilerplate.

## Choices a program makes

jam set some things with globals for a whole build; here each program chooses through the libraries it links:
- library variants are always declared and built only when linked: `engine.memory.<allocator>.<debug level>`,
  `engine.shaders.vars|varsMock|varsStub`, the stub of a feature (`gameLibs.bvh`, `engine.lowLatency.stub`);
- link choices (`dagor_add_link_choice/select`): a property of the program (DAGOR_MEASURE_PERF, DAGOR_LINUX_GUI,
  DAGOR_NO_GPU, DAGOR_SHADER_VARS, DAGOR_DAS_CONSOLE, DAGOR_LOW_LATENCY) picks the implementation, also for libraries
  in between.
- Custom transitive properties carry what a program collects from its whole link closure: DAGOR_LICENSE_FILES (its
  LICENSE-<program> file), DAGOR_RUNTIME_FILES (SDK DLLs copied next to it), DAGOR_GAME_PULLS.

## Platforms

Platforms come from CMake: CMAKE_SYSTEM_NAME, WIN32, LINUX, APPLE, IOS, ANDROID, the compiler IDs. `DAGOR_PLATFORM`
and `DAGOR_ARCH` only name output dirs. Toolchain files (presets) pick the compiler: clang-cl (pinned LLVM) or MSVC on
Windows, clang (pinned) or gcc on Linux, Apple clang, the NDK for Android. Platform defines, flags and system
libraries are in platform/<System>.cmake.

## SDKs and host tools

- SDKs are Find modules (cmake/find: DXC, Agility, NVAPI, AGS, Aftermath, FidelityFX, Astcenc, Oodle, Streamline)
  that honour `<Pkg>_ROOT` and otherwise fetch the version pinned (SHA256) in sdk/manifest.cmake into
  DAGOR_DEPS_DIR. No Gaijin hosts.
- Build steps that run engine tools (shader compilers, vromfsPacker, daBuild, the parser generators) get them from
  `dagor_host_tool()`: the tree's own target in an engine tree, otherwise the engine's host cdk/assets tree built on
  demand under a lock (scripts/build_preset.cmake), or a prebuilt CDK (DAGOR_HOST_TOOLS_DIR).
- daScript AOT: the project's `<host>-aot-compiler` tree makes `<game>-aot`, built on demand like the host tools; the
  game trees translate their daScript with it in batches (`DAS_FILES` + `DAS_PULL`).

## Games

A project's prog/CMakeLists.txt finds the engine (`find_package(Dagor)`, which adds prog/ as a subproject compiled with
the game's settings) and declares the game with `dagor_add_dng_game()`: daNetGame's main, the code game.jam generated
(gameproj::, auth keys, the pull of every module) and the libraries of danetgamelibs.txt/gamelibs.txt, whose
`_lib.cmake` add what they need. The program goes to `<project>/game/<platform>-<arch>`, the content (target `content`
of the client tree, `dagor_add_dng_content`) into `<project>/game`, packages through CPack (`dagor_package_game`, app
bundles on macOS). Switches jam turned off in Rel only (the editor, webui, ImGui, the console) are generator
expressions, so one tree builds every configuration.

Projects start from templates/ (`dng.py new`): sp-3d, mp-3d, sp-2d and mp-2d, layered from `_common`,
`_singleplayer`/`_multiplayer` and `_2d`/`_3d` so no file exists twice. A single-player game has no dedicated tree: its
client is its own server and runs the ECS tests headless on the stub driver; the presets dng.py writes have the trees
the template's `multiplayer` asks for. The templates are not built in place; CI creates a project from each.

## What differs from jam

- Tools jam always built in rel (binBlk, ddsx2dds, ddsxCvt, dolphin, whale, the ddsxConv plugins) build in the tree's
  configuration under jam's file names (NO_CONFIG_POSTFIX).
- Generated sources (ES codegen, parsers, ISPC headers, stringified files) go to the build dir, never the source tree.
- MSVC links without identical-code folding (/OPT:NOICF): daFrameGraph compares function addresses.
- daNetGame's precompiled header is used in every configuration (Ninja cannot have one in some only).
- jam's `if $(X) in a b` is true when X is unset; the build keeps what jam built (CppStcode both, quirrelHost's
  ENABLE_RE_USE=0 only under the non-ASan sanitizers).
- One library where jam built per-program flavors with globals: the physics engine of vehiclePhys
  (`gameLibs.vehiclePhys.jolt` and `.bullet`), the ImGui test engine hooks (link choices), the per-tree settings of
  the editors (one tree for all of them: the union of their drivers).

jam itself is gone from the repository (its rules, jamfiles, the committed ES codegen output); upstream still builds
with it, so this document keeps the names of jam's settings where they explain a choice. The shader compilers'
`-cppStcode` writes a CMake project of the generated state code (`_stcodeTemplates/CMakeLists.txt.fmt`) and builds it
with `scripts/build_stcode.cmake` and the platform's toolchain.

## Not ported

Upstream's jamfiles below have no CMakeLists: what they build needs what the repository does not have, or was jam's
own.

- CEF-based: `3rdPartyLibs/cef3/v4951/libcef_dll`, `1stPartyLibs/webbrowser` (+ `helper`), `gameLibs/webBrowserHelper`,
  `gameLibs/daRg/browser`, `gameLibs/quirrel/sqWebBrowser`: the CEF binary SDK (jam took it from Gaijin's devtools);
  their stubs are ported.
- FMOD Studio: `gameLibs/soundSystem` (+ `voice`, `quirrel`), `gameLibs/daRg/soundSystem`: the SDK is proprietary;
  the stubs are ported (DAGOR_GAME_SOUND stays off).
- `engine/drv/vr_device/openXr`: the OpenXR SDK (jam: OpenXrSdkPath); the null and emulator devices are ported.
- `1stPartyLibs/yuplay2auth`: Gaijin's launcher authentication; `1stPartyLibs/yuplay2` and `3rdPartyLibs/Tencent` are not
  in the repository.
- `3rdPartyLibs/webrtc-apm` (+ `avx2`): its WebRTC sources are not in the repository (upstream's neither).
- `3rdPartyLibs/assimp`: no program of the repository links it.
- `3rdPartyLibs/phys/bullet-3/test/*`: Bullet's own upstream tests (gtest), not the engine's.
- tvOS (`engine/drv/hid_tvOS`, `gameLibs/webui/plugins/tvOS`): not a platform of the engine.
- Tools of jam's workflow: `tools/miscUtils/fastdep` (jam's dependency scanner), the other utilities of
  `tools/sceneTools/utils` (binBlk is ported), the bsdiff tools of `gameLibs/compressionUtils`, Quirrel's
  `sq_llvm_fuzzer` and `bench/vmperf` (which replays a jam build).
- jam's own: the util jamfiles that listed others (`engine/daECS`, `gameLibs/ecs`, `tools/converters`,
  `tools/sceneTools`), `gameLibs/vehiclePhys/vehiclePhys-*` (now targets of `gameLibs/vehiclePhys`).
