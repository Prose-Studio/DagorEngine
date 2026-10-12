# Android: the target definitions and link settings (included by DagorCompilerFlags.cmake, whose helpers and conditions
# it uses). The NDK's toolchain file sets the ABI, API level and STL.
dagor_compile_definitions(1 _TARGET_ANDROID ANDROID_NDK ANDROID _TARGET_64BIT _TARGET_ARCH_ARM64 _TARGET_SIMD_NEON)
dagor_compile_definitions("${_cxx}" __STDC_INT64__)
dagor_compile_options("${_c_cxx}" -fpic -fno-data-sections -Wno-pointer-sign -Wno-varargs -Wno-pointer-bool-conversion
  -Wno-nullability-completeness -Wno-c++17-compat-mangling -Wno-unsupported-floating-point-opt -Wno-ignored-pragmas)
dagor_link_options("${_linked}" LINKER:--gc-sections LINKER:-z,noexecstack)
dagor_system_library(log android)
foreach(_lib System::log System::android System::dl System::m)
  link_libraries("$<${_linked}:${_lib}>")
endforeach()
unset(_lib)
