## How to Build: Environment
Requirements for building and using the Dagor Engine toolkit: Windows 10 (x64), 16 GB of RAM, 200 GB of HDD/SSD space.

* Install Git: https://git-scm.com/download/win
* Install 7-Zip: https://www.7-zip.org/
* Install Python 3
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

Run `dagor.py devtools`. This will download, install, and configure the build toolkit. You should provide the path to the build toolkit folder as an argument, and the script will create this folder if it doesn't exist.

```
python3 dagor.py devtools X:\develop\devtools
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

Run `python3 dagor.py build` in DagorEngine root.

This builds the entire project toolkit from the source code. This process may take a considerable amount of time.
After tools are built and ready to be used script builds game and UI resources using daBuild and other utilities.
The data the tools need that is not built (editor icons, fonts, themes, dargbox UI) is copied from prog/tools/toolsData into tools/, so nothing has to be downloaded.

`dagor.py build` and the projects' `build.py` scripts accept optional parameters to limit components to be built:
`code`, `shaders`, `assets`, `vromfs`, `gui`.
If no parameters are passed, all components are built.

They also accept optional parameters to force target architecture to be built, e.g. `arch:x86_64`, `arch:arm64`, `arch:x86`.
If none is specified code is built to default architecture (depends on host OS and jamfile settings).

`dagor.py build` in addition to components accepts optional list of projects to be built:
`project:dagorTools`, `project:dargbox`, `project:physTest`.
If none is passed, all projects are built.

Example: `dagor.py build project:dargbox code shaders` will build only code and shaders for **dargbox**.

### Documentation
  Automatically generated [Dagor Documentation](https://prose-studio.github.io/DagorEngine/) contains general architecture description, API reference, tutorials and manuals.<br>
  It is not complete yet and will be extended.

## Open-source roadmap

We are going to open-source more parts of our Engine and tools.
These are general and broad plans for next year, can be changed.

### Documentation

* how to work with dagor assets
* daNetGame framework
