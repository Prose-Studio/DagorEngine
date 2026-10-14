# Build System

How the engine and its projects are organized for CMake. Each function's
reference is the comment at the top of its module in `prog/cmake`.

## Layout

```text
prog/CMakeLists.txt       the engine: project(DagorEngine), include(cmake/Dagor.cmake), the areas
prog/CMakePresets.json    the engine's trees (cmake --list-presets), on cmake/presets/base.json
prog/cmake/               Dagor.cmake (the entry), DagorConfig.cmake (find_package(Dagor)), the Dagor*.cmake
                          modules, platform/<CMAKE_SYSTEM_NAME>.cmake, toolchains/, presets/, find/ (SDKs),
                          sdk/manifest.cmake, scripts/, templates/
<project>/prog/CMakeLists.txt + CMakePresets.json   a game (templates/, dng.py new)
```

`prog/` is the engine's top level; there is no `CMakeLists.txt` at the
repository root. Build trees are `build/<preset>` next to `prog/` (of the engine
or of a project), and only intermediates go there: the tools are installed into
`tools/`, a game's programs and content go to the project's `game/`.

## Trees and Presets

A tree is a preset: a target platform and compiler (the hidden `toolchain-*`
bases of `cmake/presets/base.json`, each with its toolchain file) and a variant,
`DAGOR_VARIANT`, which sets the defaults of the options (`DagorOptions.cmake`).
The `<host>[-<compiler>|-<arch>]` presets (`windows`, `linux-clang`, ...) are a
tree of their own that builds every tree of that platform and compiler with its
preset, one after the other (`DagorAll.cmake`, `DAGOR_ALL_PRESETS`), and
installs the tools. A project's `<host>` workflow likewise builds the client,
its content and a multiplayer game's dedicated server.

| variant | builds by default |
|---|---|
| `tests` | the engine's unit tests (CTest) |
| `cdk` | the command-line tools of the content pipeline on the static kernel and the dag4blend add-on; the `cdk` install component puts them in `tools/dagor_cdk/<platform>-<arch>` (the add-on in `tools/dagor_cdk/universal`) |
| `assets` | the asset build on daKernel (the shared kernel): daBuild with its exporter plugins, ddsxCvt2 |
| `editor` | the GUI editors on daKernel: impostorBaker; daEditor3x with its plugins and AssetViewer on Windows and Linux; blkEditor and plodGen on Windows |
| `dargbox` | the daRg sandbox with its shaders and vromfs, in `tools/dargbox`; cross-built, its APK (`android-dargbox`, `dagor_android_apk`) and its iOS app bundle (`ios-dargbox`) |
| `maxplug` | opt-in, not in the `windows` preset: the 3ds Max plugin of each 3ds Max SDK found, 2025 and later (`DAGOR_MAX_VERSIONS`, `MaxSDK_<version>_ROOT`) |
| `game` | a project's game: its presets `<host>-client`, `<host>-dedicated`, `<host>-aot-compiler` |

The configurations are Dev (optimized, with logs and asserts), Rel, IRel (Rel
without any logs) and Dbg (unoptimized), all in one Ninja Multi-Config tree.
Workflow presets chain configure, build and test (or package).

`DAGOR_COMPILER_LAUNCHER=sccache` in the environment (or the cache) of a new
tree compiles through sccache, the pinned one fetched into `DAGOR_DEPS_DIR`; it
keeps the objects of every tree and project in one cache (`SCCACHE_DIR`), so a
rebuild, another worktree or another project compiles only what changed. CI
builds that way. A path there names another launcher (ccache).

Variants are separate trees for what one tree cannot hold: the kernel linkage
(static in cdk and tests, daKernel in assets and editor) and the 3D driver
interface, whose `_TARGET_D3D_MULTI` applies to all the code of a tree. The
assets tree's programs link the null driver directly; the editors' and
dargbox's link the platform's drivers through the multi-driver interface. The
editors are games on daNetGame (daEditor3x is `editor_dng`, AssetViewer
`asset_viewer_dng`, each with its list of daNetGameLibs) with the game features
off; the editor tree builds daNetGame for them like a game tree.

## Targets

One `CMakeLists.txt` per module directory, one `dagor_add_target()` call per
target in it:

```cmake
dagor_add_target(NAME engine.math STATIC
  FILES_CMAKE math_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
)
```

- The sources are in `<name>_files.cmake` next to it (`FILES`, `ES_FILES`,
  `DAS_FILES`, `STRINGIFY_FILES`, `STRINGIFY_ARRAY_FILES`);
  `<name>_<platform>_files.cmake` adds a platform's (windows, linux, macos, ios,
  android; apple for both Apple platforms) and `<name>_<platform>.cmake` its
  settings. Adding or removing a source edits a `_files.cmake`; a
  `CMakeLists.txt` changes only when targets or dependencies do.
- The areas (`3rdPartyLibs`, `1stPartyLibs`, `engine`, `commonFx`, `gameLibs`,
  `daNetGameLibs`, `tools`) add every module directory themselves, by relative
  path, under the conditions it builds on. Module directories add none, so no
  variable leaks from one module into another.
- Targets are named after their directory under `prog/` with dots
  (`engine.math`); a few have `Dagor::` aliases for what projects link
  (`Dagor::Quirrel`, `Dagor::Phys`). `CMAKE_LINK_LIBRARIES_ONLY_TARGETS` is on,
  so a misspelled dependency is a configure error. System libraries and Apple
  frameworks are `System::<name>` imported targets (`DagorSystemLibs.cmake`).
- Kinds: STATIC (the default), OBJECT, SHARED, MODULE, HEADERONLY (an INTERFACE
  library), EXECUTABLE [APPLICATION] [MACOSX_BUNDLE]. INTERFACE and WIN32 are
  spelt HEADERONLY and APPLICATION because the scope `INTERFACE` and the define
  `WIN32` are values of the other keywords.
- Kinds of target with more to them are functions with the same arguments:
  `dagor_add_catch2_test`, `dagor_add_dng_module`, `dagor_add_dng_game`,
  `dabuild_plugin`, `dsc2_compiler`. They append their own `FILES_CMAKE` and
  `BUILD_DEPENDENCIES` to the caller's (repeated multi-value keywords
  accumulate).
- Libraries are built for the programs that link them (EXCLUDE_FROM_ALL); the
  variant names its programs (`dagor_build_by_default`, `prog/CMakeLists.txt`); a
  project's programs are built by default.
- First-party code gets the strict warning set (errors with
  `DAGOR_WARNINGS_AS_ERRORS`); LAX gives third-party code the lax one. Settings
  of a whole tree are directory-level (`DagorCompilerFlags.cmake` and
  `platform/`), not per-target boilerplate.
- Generated sources (ES codegen, parsers, ISPC headers, stringified files, the
  shader compilers' C++ state code) go to the build tree, never the source tree.
- Tools whose file names have no configuration suffix (binBlk, ddsx2dds,
  ddsxCvt, dolphin, whale, the ddsxConv plugins) build in the tree's
  configuration (`NO_CONFIG_POSTFIX`).

## Choices a Program Makes

Each program chooses through the libraries it links:

- Library variants are always declared and built only when linked:
  `engine.memory.<allocator>.<debug level>`,
  `engine.shaders.vars|varsMock|varsStub`, the stub of a feature (`gameLibs.bvh`,
  `engine.lowLatency.stub`), the physics engine of vehiclePhys
  (`gameLibs.vehiclePhys.jolt` and `.bullet`).
- Link choices (`dagor_add_link_choice` and `dagor_add_link_select`): a property
  of the program (`DAGOR_MEASURE_PERF`, `DAGOR_LINUX_GUI`, `DAGOR_NO_GPU`,
  `DAGOR_SHADER_VARS`, `DAGOR_DAS_CONSOLE`, `DAGOR_LOW_LATENCY`, `DAGOR_VR`)
  picks the implementation, also for the libraries in between.
- Custom transitive properties carry what a program collects from its whole link
  closure: `DAGOR_LICENSE_FILES` (its `LICENSE-<program>` file),
  `DAGOR_RUNTIME_FILES` (SDK DLLs copied next to it), `DAGOR_GAME_PULLS`.

## Platforms

Platforms come from CMake: `CMAKE_SYSTEM_NAME`, `WIN32`, `LINUX`, `APPLE`,
`IOS`, `ANDROID` and the compiler IDs. `DAGOR_PLATFORM` and `DAGOR_ARCH` only
name output directories. The toolchain files the presets name pick the compiler:
clang-cl (the pinned LLVM) or MSVC on Windows, clang (pinned) or GCC on Linux,
Apple clang on macOS and iOS, the NDK's clang for Android. Platform defines,
flags and system libraries are in `platform/<System>.cmake`.

## SDKs and Host Tools

- SDKs are Find modules (`cmake/find`) that honour `<Pkg>_ROOT` and otherwise
  fetch the version pinned with its SHA256 in `sdk/manifest.cmake` into
  `DAGOR_DEPS_DIR`, from the vendor's own release.
- Proprietary SDKs are never fetched: you install them, and what needs them is
  off until you do. The FMOD Engine (FMOD Studio API, `FMOD_ROOT`, by default
  where its installer puts it) for the games' sound (`DAGOR_GAME_SOUND`); the
  3ds Max SDKs (`MaxSDK_<version>_ROOT`) for the `maxplug` preset.
- Build steps that run engine tools (shader compilers, vromfsPacker, daBuild, the
  parser generators) get them from `dagor_host_tool()`: the tree's own target in
  an engine tree, otherwise the engine's host cdk or assets tree, built on demand
  under a lock (`scripts/build_preset.cmake`), or a prebuilt CDK
  (`DAGOR_HOST_TOOLS_DIR`).
- daScript AOT: the project's `<host>-aot-compiler` tree makes `<game>-aot`,
  built on demand like the host tools; the game trees translate their daScript
  with it in batches (`DAS_FILES` and `DAS_PULL`).
- Content: `dagor_add_shaders()` compiles a shader blk when the compiler or a
  source changes; `dagor_add_content_step()` runs a tool that tracks its own
  inputs (the game's shaders, vromfs, daBuild).

## Games

A project's `prog/CMakeLists.txt` finds the engine (`find_package(Dagor)`, which
adds `prog/` as a subproject compiled with the game's settings) and declares the
game with `dagor_add_dng_game()`: daNetGame's main, the generated game code
(`gameproj::`, auth keys, the pull of every module) and the libraries of
`danetgamelibs.txt` and `gamelibs.txt`, whose `_lib.cmake` files add what they
need. The program goes to `<project>/game/<platform>-<arch>`, the content
(target `content` of the client tree, `dagor_add_dng_content`) into
`<project>/game`; packages are made with CPack (`dagor_package_game`, app
bundles on macOS). The switches that are off in Rel builds only (the editor,
webui, ImGui, the console) are generator expressions, so one tree builds every
configuration.

The game's options are cache variables of its trees (the project presets set
them): `DAGOR_GAME_SOUND` (FMOD), `DAGOR_GAME_EMBEDDED_BROWSER` (CEF in the
Windows client, its `cefprocess` and runtime next to the game),
`DAGOR_GAME_ASSET_MANAGER` (on in Windows clients: daBuild built into them,
outside Rel, builds the assets the game loads from the project's sources and
rebuilds and reloads those that change, with `assets_import` in `gamelibs.txt`
and a `base_asset_manager` entity; its templates derive from the game's
`rendinst` and `animchar`), and the crash reports:
`DAGOR_BREAKPAD` (on in Windows and Linux clients, for Rel builds),
`DAGOR_BREAKPAD_SUBMISSION` (every configuration, with the bpreport sender,
on FLTK, next to the game) and `DAGOR_CRASHPAD` (Windows, instead of
breakpad).

Projects start from `templates/` (`dng.py new`): sp-3d, mp-3d, sp-2d and mp-2d,
layered from `_common`, `_singleplayer` or `_multiplayer`, and `_2d` or `_3d`,
so no file exists twice. A single-player game has no dedicated tree: its client
is its own server and runs the ECS tests headless on the stub driver. The
templates are not built in place; CI creates a project from each.
