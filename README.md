## How to Build: Environment

The engine builds with CMake on Windows 10/11 (x64, arm64), Linux (x86_64, arm64) and macOS (arm64, x64), and cross
builds for Android and iOS. Building the engine tools takes 16 GB of RAM and 200 GB of disk space.

* Git, Python 3.8 or newer, CMake 4.0 or newer and Ninja (`python -m pip install cmake ninja` gives both)
* Windows: Visual Studio 2022 (or its Build Tools) with the C++ workload and a Windows 10/11 SDK; the engine compiles
  with the pinned LLVM (clang-cl), which the configure fetches, or with MSVC (the `windows-msvc-*` presets)
* Linux: GCC 11+ or Clang, and the development packages: `libx11-dev libxrandr-dev libxi-dev libxcursor-dev
  libxkbcommon-dev libfltk1.3-dev libxkbfile-dev libudev-dev libpulse-dev libasound2-dev libdbus-1-dev uuid-dev nasm`
  (Debian/Ubuntu names)
* macOS: Xcode 16 or newer

The SDKs the build needs (DirectX Shader Compiler, ISPC, Vulkan headers, LLVM, ...) are downloaded once, checked against
pinned SHA256 sums, into `DAGOR_DEPS_DIR` (by default `%LOCALAPPDATA%/dagor`, `~/Library/Caches/dagor` or
`~/.cache/dagor`); the 3ds Max SDKs (2025 and later), which are not redistributable, are used only by the opt-in
`windows-maxplug` tree, where they are installed (`MaxSDK_<version>_ROOT` points it at another dir).

Clone the source code into a path without spaces or non-Latin characters:
```
git clone https://github.com/Prose-Studio/DagorEngine.git
cd DagorEngine/prog
```

## How to Build: Build from Source Code

On a fresh clone, one command builds everything for the host: it fetches the SDKs and builds and installs every tree
(the tests, the tools, the asset build, the editors, dargbox):

```
cmake --workflow --preset windows              (linux, macos; windows-msvc, linux-clang, windows-arm64, ...)
```

Each tree also has its own presets in `prog/CMakePresets.json` (`cmake --list-presets` lists them), in
`build/<preset>`:

```
cmake --workflow --preset windows-tests        the engine and its tests
cmake --workflow --preset windows-cdk          the tools: shader compilers, packers, converters
cmake --workflow --preset windows-assets       daBuild and its exporters
cmake --workflow --preset windows-editor       the editors: daEditor, AssetViewer, impostorBaker
cmake --workflow --preset windows-dargbox      the UI tool, its shaders and vromfs
cmake --workflow --preset windows-maxplug      opt-in: the 3ds Max plugin of each Max SDK installed (2025 and later)
```

(`linux-` and `macos-` on those hosts; `windows-msvc-`, `linux-clang-`, `windows-arm64-`, `macos-universal-` and the
sanitizer presets build the others.) The tools are installed into `tools/dagor_cdk/<host>-<arch>`. The data the tools
load at runtime and that is not built (the editors' `commonData`, dargbox's fonts and UI, ...) is part of the
repository, in `prog/tools/toolsData`: nothing has to be downloaded. See
[Build System](_docs/source/getting-started/build_system.md) for how the build is organized.

Then create a game project from a template (single-player or multiplayer, 3D or 2D), see
[Creating a Project](_docs/source/getting-started/new_project.md):
```
cd ..
python dng.py new --template sp-3d --name MyGame --dest ../MyGame
```

A game project has this layout:
```
<project>/game
         /develop
         /prog
```

* prog - game source code, its CMakeLists.txt and CMakePresets.json
* develop - initial assets
* game - directory where assets are placed after building and game executable files are located

### Documentation
  Automatically generated [Dagor Documentation](https://gaijinentertainment.github.io/DagorEngine/) contains general architecture description, API reference, tutorials and manuals.<br>
  It is not complete yet and will be extended.

## Open-source roadmap

We are going to open-source more parts of our Engine and tools.
These are general and broad plans for next year, can be changed.

### Documentation

* how to work with dagor assets
* daNetGame framework
