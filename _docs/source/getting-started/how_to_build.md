# How to Build

## How to Build: Environment

```{important}
Requirements for building and using the Dagor Engine toolkit:
- Windows 10 (x64)
- 16&nbsp;GB of RAM
- 200&nbsp;GB of HDD/SSD space
```

1. Install Git: <https://git-scm.com/download/win>.

2. Install 7-Zip: <https://www.7-zip.org/>.

3. Install Python 3.

4. If you plan to use the FMOD sound library, also install FMOD Studio SDK
   2.02.15.

5. Create a project directory at the root of any drive.

   ```{note}
   The directory name should not contain spaces or non-Latin characters.
   ```

   ```text
   md X:\develop
   cd X:\develop
   ```

6. Clone the Dagor Engine source code and samples:

   ```text
   git clone https://github.com/Prose-Studio/DagorEngine.git
   cd DagorEngine
   ```

7. Run `dagor.py devtools`.

   This will download, install, and configure the build toolkit. You
   should provide the path to the build toolkit directory as an argument, and
   the script will create this directory if it doesn't exist.

   ```text
   python3 dagor.py devtools X:\develop\devtools
   ```

   ```{important}
   - If the script is not run as an administrator, installers of certain
     programs may request permission for installation, which you should grant.
   - If you plan to use plugins for 3ds Max, press `Y` when the script asks if
     you want to install the 3ds Max SDK.
   - The script will also ask to add the path `X:\develop\devtools` to the
     `PATH` environment variable and set the `GDEVTOOL` variable to point to
     this directory.
   ```

   After the script completes its work, the `X:\develop\devtools` directory will
   be configured with the following SDKs and tools:

   - `FidelityFX_SC`: a library for image quality enhancement
   - `fmod-studio-2.xx.xx` [optional]: FMOD sound library
   - `LLVM-15.0.7`: C/C++ compiler and libraries (Clang)
   - `nasm`: assembler
   - `max2024.sdk`: 3ds Max 2004 SDK
   - `openxr-1.0.16`: library for AR/VR
   - `vc2019_16.10.3`: C/C++ compiler and libraries (MSVC)
   - `win.sdk.100`: Windows 10 SDK
   - `win.sdk.81`: Windows 8.1 SDK
   - `ducible.exe`: a tool to make builds of Portable Executables (PEs) and PDBs
     reproducible
   - `pdbdump.exe`: a tool for dumping the content of PDB files
   - `jam.exe`: a small build tool that can be used as a replacement for Make

8. Restart the command line console to make the new environment variables
   available.

## How to Build: Build from Source Code

Run `python3 dagor.py build` in `DagorEngine` to build the entire engine toolkit
from the source code. This process may take a considerable amount of time.

It also copies the data the tools need that is not built (editor icons, fonts,
themes, dargbox UI) from `prog/tools/toolsData` into `tools`, so nothing has to
be downloaded.

The directory structure should look like this:

```text
develop
└── DagorEngine
    ├── prog
    ├── tools
    └── _docs
```

```{seealso}
For more information, see
[Directory Structure Overview](directory_structure.md).
```


