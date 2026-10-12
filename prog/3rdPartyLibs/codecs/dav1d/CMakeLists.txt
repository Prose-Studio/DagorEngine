# dav1d, the AV1 video decoder (8-bit), with its x86 (NASM) and arm64 assembly; the configs of each platform are in
# generated/
set(includes ${CMAKE_CURRENT_SOURCE_DIR} src generated include include/common include/dav1d tools)
if(DAGOR_ARCH STREQUAL "x86_64" AND WIN32)
  list(APPEND includes generated/win64)
endif()
if(WIN32 AND DAGOR_ARCH STREQUAL "arm64")
  list(APPEND includes generated/windows_arm64)
endif()
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  if(DAGOR_ARCH STREQUAL "arm64")
    list(APPEND includes generated/macosx_arm64)
  else()
    list(APPEND includes generated/macosx_x86_64)
  endif()
endif()
if(IOS)
  list(APPEND includes generated/macosx_arm64)
endif()
if(LINUX)
  list(APPEND includes generated/linux)
  list(APPEND libs System::pthread)
endif()
if(ANDROID)
  if(DAGOR_ARCH STREQUAL "arm64")
    list(APPEND includes generated/android/aarch64)
  else()
    list(APPEND includes generated/android/arm)
  endif()
endif()
if(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  list(APPEND includes include/compat/msvc) # stdatomic.h and the like
endif()
if(LINUX AND NOT (CMAKE_CXX_COMPILER_ID MATCHES "Clang" AND NOT MSVC))
  list(APPEND includes include/compat/gcc)
endif()
# the assembly's symbol names: underscore-prefixed on Apple (the target and minimum OS of the ASM compiler come from
# the toolchain there)
set(asm_options)
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin" AND DAGOR_ARCH STREQUAL "x86_64")
  list(APPEND asm_options "$<$<COMPILE_LANGUAGE:ASM_NASM>:SHELL:--prefix _>")
elseif(APPLE)
  list(APPEND asm_options "$<$<COMPILE_LANGUAGE:ASM>:-DPREFIX>")
endif()
list(APPEND c_options -DBITDEPTH=8)
if(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  list(APPEND c_options /wd4028 /wd4244 /wd4267 /wd4996 /wd4090 /wd4133)
elseif(DAGOR_ARCH STREQUAL "e2k")
  list(APPEND c_options
    -w167
    -w513
    -Wno-bad-initializer-type
    -Wno-incompatible-pointer-types
    -Wno-reduced-alignment
  )
else()
  list(APPEND c_options -Wno-incompatible-pointer-types)
endif()

dagor_add_target(NAME 3rdPartyLibs.codecs.dav1d STATIC LAX
  FILES_CMAKE dav1d_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_OPTIONS PRIVATE ${asm_options} "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
  BUILD_DEPENDENCIES PUBLIC ${libs}
)
