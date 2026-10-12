# The target platform as the engine names it in paths, and the languages its sources use.
#
#   DAGOR_PLATFORM  windows, linux, macOS, iOS or android: the names of jam's output dirs (<project>/game/<platform>-<arch>,
#                   tools/dagor_cdk/<platform>-<arch>). Code tests the platform with CMake's own variables (WIN32,
#                   LINUX, APPLE, IOS, ANDROID, CMAKE_SYSTEM_NAME) or $<PLATFORM_ID:...>.
#   DAGOR_ARCH      x86_64, arm64, e2k or universal (macOS: both archs in one binary), from the toolchain.
#   DAGOR_DATA_FORMAT  the format code of the target's packed resources (PC, iOS, and).
include_guard(GLOBAL)

if(CMAKE_SYSTEM_NAME STREQUAL "Windows")
  set(DAGOR_PLATFORM windows)
elseif(CMAKE_SYSTEM_NAME STREQUAL "Linux")
  set(DAGOR_PLATFORM linux)
elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  set(DAGOR_PLATFORM macOS)
elseif(CMAKE_SYSTEM_NAME STREQUAL "iOS")
  set(DAGOR_PLATFORM iOS)
elseif(CMAKE_SYSTEM_NAME STREQUAL "Android")
  set(DAGOR_PLATFORM android)
else()
  message(FATAL_ERROR "The engine does not build for ${CMAKE_SYSTEM_NAME}")
endif()

if(NOT DAGOR_ARCH)
  message(FATAL_ERROR "DAGOR_ARCH is not set: configure with a preset, whose toolchain file sets it")
endif()
set(_dagor_archs_windows x86_64 arm64)
set(_dagor_archs_linux x86_64 arm64 e2k)
set(_dagor_archs_macOS x86_64 arm64 universal)
set(_dagor_archs_iOS arm64)
set(_dagor_archs_android arm64)
if(NOT DAGOR_ARCH IN_LIST _dagor_archs_${DAGOR_PLATFORM})
  message(FATAL_ERROR "DAGOR_ARCH=${DAGOR_ARCH} is not an arch of ${DAGOR_PLATFORM} (${_dagor_archs_${DAGOR_PLATFORM}})")
endif()
unset(_dagor_archs_windows)
unset(_dagor_archs_linux)
unset(_dagor_archs_macOS)
unset(_dagor_archs_iOS)
unset(_dagor_archs_android)

if(IOS)
  set(DAGOR_DATA_FORMAT iOS)
elseif(ANDROID)
  set(DAGOR_DATA_FORMAT and)
else()
  set(DAGOR_DATA_FORMAT PC)
endif()

# the assemblers, by extension as in jam: .asm/.nasm/.nas NASM, .masm MASM (Windows x86_64), .s/.S the GNU assembler (the
# C compiler; LLVM's clang on Windows arm64). Enabled here, in the top-level directory, for every target of the tree.
set(CMAKE_ASM_NASM_SOURCE_FILE_EXTENSIONS asm nasm nas)
set(CMAKE_ASM_MASM_SOURCE_FILE_EXTENSIONS masm)
set(CMAKE_ASM_SOURCE_FILE_EXTENSIONS s S)
if(WIN32 OR (CMAKE_SYSTEM_NAME STREQUAL "Darwin" AND NOT DAGOR_ARCH STREQUAL "arm64"))
  dagor_fetch_sdk(nasm _dagor_nasm)
  find_program(CMAKE_ASM_NASM_COMPILER NAMES nasm PATHS "${_dagor_nasm}" NO_DEFAULT_PATH REQUIRED)
  unset(_dagor_nasm)
else()
  find_program(CMAKE_ASM_NASM_COMPILER NAMES nasm) # the distro's; only the libraries with NASM sources need it
endif()
if(CMAKE_ASM_NASM_COMPILER)
  enable_language(ASM_NASM)
endif()
if(WIN32)
  if(DAGOR_ARCH STREQUAL "x86_64")
    enable_language(ASM_MASM)
  elseif(DAGOR_LLVM_DIR)
    set(CMAKE_ASM_COMPILER "${DAGOR_LLVM_DIR}/bin/clang${CMAKE_HOST_EXECUTABLE_SUFFIX}")
    set(CMAKE_ASM_COMPILER_TARGET aarch64-pc-windows-msvc)
    enable_language(ASM)
  endif()
  enable_language(RC)
else()
  enable_language(ASM)
endif()
if(APPLE)
  enable_language(OBJC OBJCXX)
endif()

# the platform's definitions, libraries and link settings (prog/cmake/platform/<CMAKE_SYSTEM_NAME>.cmake), applied to
# the targets of this directory and those below it with the other tree settings (DagorCompilerFlags.cmake)
set(DAGOR_PLATFORM_FILE "${CMAKE_CURRENT_LIST_DIR}/platform/${CMAKE_SYSTEM_NAME}.cmake")
