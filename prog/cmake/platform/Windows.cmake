# Windows: the target definitions and the libraries every program links (included by DagorCompilerFlags.cmake, whose
# helpers and conditions it uses).
dagor_compile_definitions(1 _TARGET_PC=1 _TARGET_PC_WIN=1 WIN64 _TARGET_64BIT WIN32_LEAN_AND_MEAN= _USE_MATH_DEFINES
  NOMINMAX _ALLOW_KEYWORD_MACROS= DELAYIMP_INSECURE_WRITABLE_HOOKS)
dagor_compile_definitions("${_release}" _SECURE_SCL=0)
dagor_compile_definitions("${_cxx_no_exceptions}" _HAS_EXCEPTIONS=0)
if(DAGOR_ARCH STREQUAL "x86_64")
  dagor_compile_definitions(1 _TARGET_ARCH_X86_64)
else()
  dagor_compile_definitions(1 _TARGET_ARCH_ARM64 _TARGET_SIMD_NEON)
endif()

set(_libs System::kernel32 System::user32 System::gdi32 System::ole32 System::winmm System::dbghelp)
if(MSVC AND CMAKE_CXX_COMPILER_ID STREQUAL "Clang" AND DAGOR_ARCH STREQUAL "x86_64")
  list(APPEND _libs System::clang_rt.builtins-x86_64)
endif()
foreach(_lib IN LISTS _libs)
  link_libraries("$<${_linked}:${_lib}>")
endforeach()
unset(_lib)
unset(_libs)
