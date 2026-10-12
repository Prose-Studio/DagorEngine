## How to Build: Environment
Requirements for building and using the Dagor Engine toolkit: Windows 10 (x64), 16 GB of RAM, 200 GB of HDD/SSD space.

* Install Git: https://git-scm.com/download/win
* Install Python 3.8 or newer
* If you plan to use the FMOD sound library, also install FMOD Studio SDK 2.02.15

Create a project folder at the root of any drive (the folder name should not contain spaces or non-Latin characters).
```
md X:\develop && cd X:\develop
```

Clone the Dagor Engine source code:
```
git clone https://github.com/Prose-Studio/DagorEngine.git
cd DagorEngine
```

Everything else is done with `dng.py` in the DagorEngine root (`python dng.py <command> -h` lists the options of a command):
```
python dng.py devtools X:\develop\devtools          the build toolkit (once, then restart the console)
python dng.py build                                 the engine tools, dargbox and the project template
python dng.py new --name MyGame --dest ..\MyGame    a game project of your own
python dng.py test                                  the engine tests
```

## How to Build: Build Toolkit

Run `dng.py devtools`. It downloads, installs and configures the build toolkit. Give it the path of the build toolkit folder; it creates the folder if it doesn't exist, and skips what is already set up when run again.

```
python dng.py devtools X:\develop\devtools
```

If the script is not run as an administrator, installers of certain programs may request permission for installation, which you should grant. If you plan to use plugins for 3ds Max, press 'Y' when the script asks if you want to install the 3ds Max SDK. The script will also ask to add the path X:\develop\devtools to the PATH environment variable and set the GDEVTOOL variable to point to this folder.

After the script completes its work, the X:\develop\devtools folder will be configured with the following SDKs and tools:

* aftermath-2025.5.0.25317 - NVIDIA Nsight Aftermath
* Agility.SDK.1.619.3 - DirectX 12 Agility SDK
* AGS.SDK.6.3.0 - AMD GPU Services
* astcenc-4.6.1 - Adaptive Scalable Texture Compression (ASTC) Encoder
* DXC-1.8.2505.1 - DirectX Compiler
* FidelityFX_SC - a library for image quality enhancement
* fmod-studio-2.xx.xx [optional] - FMOD sound library
* ispc-v1.23.0-windows - Implicit SPMD Program Compiler
* LLVM-21.1.8 - C/C++ compiler and libraries (Clang)
* max2026.sdk - 3ds Max 2026 SDK
* nasm - netwide assembler ver 2.x
* openxr-1.1.54 - library for AR/VR
* streamline-2.14.1 - NVIDIA SDK for DLSS, DLAA, Reflex, etc.
* vc2019_16.11.34 - C/C++ compiler and libraries (MSVC)
* vc2022_17.14.4 - C/C++ compiler and libraries (MSVC)
* win.sdk.100 - Windows 10 SDK
* win.sdk.81 - Windows 8.1 SDK
* ducible.exe - a tool to make builds of Portable Executables (PEs) and PDBs reproducible
* pdbdump.exe - a tool for dumping the content of PDB files
* jam.exe - a small build tool (used in DagorEngine instead of Make and similar tools)

Restart the command line console to make the new environment variables available.

## How to Build: Build from Source Code

Build from the DagorEngine root:
```
python dng.py build
```

This builds the engine toolkit (`cdk`), the `dargbox` UI tool and the `dngEmpty` project template from the source code. This process may take a considerable amount of time.
After the tools are built, each project's resources are built with daBuild and the other tools.
The data the tools load at runtime and that is not built (the editors' `commonData`, dargbox's fonts and UI, ...) is part of the repository, in `prog/tools/toolsData`, and the build copies it into `tools/`: nothing has to be downloaded.

Then create a game project with `python dng.py new`, see [Creating a Project](_docs/source/getting-started/new_project.md).

Projects: `cdk`, `dargbox`, `dngEmpty`.
`-c` limits the components to build, `code`, `shaders`, `assets`, `vromfs`, `gui`, `tools` (default: everything each project builds), and `--arch` sets the target architecture, e.g. `x86_64`, `arm64` (default: the host's).

A game project has this layout:
```
<project>/game
         /develop
         /prog
```

* prog - game source code
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
