# How to Build

## How to Build: Environment

```{important}
The engine builds with CMake on Windows 10/11 (x64, arm64), Linux (x86_64,
arm64) and macOS (arm64, x64), and cross builds for Android and iOS. Building
the engine tools takes 16&nbsp;GB of RAM and 200&nbsp;GB of HDD/SSD space.
```

1. Install Git, Python 3.8 or newer, CMake 4.0 or newer and Ninja
   (`python -m pip install cmake ninja` gives both), and the platform's
   compiler:

   - Windows: Visual Studio 2022 (or its Build Tools) with the C++ workload and
     a Windows 10/11 SDK. The engine compiles with the pinned LLVM (clang-cl),
     which the configure fetches, or with MSVC (the `windows-msvc-*` presets).
   - Linux: GCC 11+ or Clang, and the development packages
     `libx11-dev libxrandr-dev libxi-dev libxcursor-dev libxkbcommon-dev
     libfltk1.3-dev libxkbfile-dev libudev-dev libpulse-dev libasound2-dev
     libcurl4-openssl-dev libssl-dev libdbus-1-dev uuid-dev nasm`
     (Debian/Ubuntu names).
   - macOS: Xcode 16 or newer.

2. Clone the Dagor Engine source code into a path without spaces or non-Latin
   characters:

   ```text
   git clone https://github.com/Prose-Studio/DagorEngine.git
   cd DagorEngine/prog
   ```

The SDKs the build needs (DirectX Shader Compiler, ISPC, Vulkan headers, LLVM,
...) are downloaded once by the configure, checked against pinned SHA256 sums,
into `DAGOR_DEPS_DIR` (by default `%LOCALAPPDATA%/dagor`,
`~/Library/Caches/dagor` or `~/.cache/dagor`). The 3ds Max SDK, which is not
redistributable, is used when you point the build at it (`MaxSDK_ROOT`, for the
`windows-maxplug` presets).

## How to Build: Build from Source Code

The engine is built with the CMake presets of `prog/CMakePresets.json`
(`cmake --list-presets` lists them), each one a tree in `build/<preset>`:

```text
cmake --workflow --preset windows-tests-ci     the engine and its tests (those that need no GPU)
cmake --workflow --preset windows-cdk          the tools: shader compilers, packers, converters
cmake --workflow --preset windows-assets       daBuild and its exporters
cmake --workflow --preset windows-editor       the editors: daEditor, AssetViewer, impostorBaker
cmake --workflow --preset windows-dargbox      the UI tool
```

Use `linux-` and `macos-` on those hosts; `windows-msvc-`, `linux-clang-`,
`windows-arm64-`, `macos-universal-` and the sanitizer presets build the
others. The tools are installed into `tools/dagor_cdk/<host>-<arch>`. The data
the tools load at runtime and that is not built (the editors' `commonData`,
dargbox's fonts and UI) is part of the repository, in `prog/tools/toolsData`.
`prog/cmake/DESIGN.md` describes how the build is organized.

To start a game of your own, see [Creating a Project](new_project.md).
