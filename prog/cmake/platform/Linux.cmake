# Linux: the target definitions and link settings (included by DagorCompilerFlags.cmake, whose helpers and conditions
# it uses).
dagor_compile_definitions(1 _TARGET_PC=3 _TARGET_PC_LINUX=3 _TARGET_64BIT __LINUX__=64 _POSIX_C_SOURCE=200809L
  _GNU_SOURCE __STDC_CONSTANT_MACROS)
if(DAGOR_ARCH STREQUAL "arm64")
  dagor_compile_definitions(1 _TARGET_ARCH_ARM64 _TARGET_SIMD_NEON)
else()
  dagor_compile_definitions(1 _TARGET_ARCH_X86_64) # e2k too: its lcc compiles the x86_64 intrinsics
endif()
if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
  dagor_compile_definitions(1 __vectorcall=)
endif()
if(DAGOR_ARCH STREQUAL "e2k")
  dagor_compile_definitions(1 _XM_NO_INTRINSICS_)
endif()
if(DAGOR_SANITIZE STREQUAL "thread" AND CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  dagor_compile_definitions(1 __SANITIZE_THREAD__) # gcc defines __SANITIZE_ADDRESS__ but not this one
endif()

dagor_link_options("${_linked}" -pipe -rdynamic LINKER:--gc-sections LINKER:-z,noexecstack LINKER:-z,separate-code)
# programs load the shared libraries next to them (daKernel, an SDK's runtime files), built and installed
set(CMAKE_BUILD_RPATH "$ORIGIN")
set(CMAKE_INSTALL_RPATH "$ORIGIN")
foreach(_lib Threads::Threads System::dl System::rt System::m)
  link_libraries("$<${_linked}:${_lib}>")
endforeach()
unset(_lib)
