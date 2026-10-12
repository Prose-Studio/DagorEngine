# BLAKE3 hashing with the SIMD implementations of the target (MASM on Windows x64, GNU assembly elsewhere)
set(defines)
if(DAGOR_ARCH STREQUAL "e2k")
  set(defines BLAKE3_NO_SSE2 BLAKE3_NO_SSE41 BLAKE3_NO_AVX2 BLAKE3_NO_AVX512)
elseif(DAGOR_ARCH STREQUAL "x86_64" AND WIN32)
  set(defines BLAKE3_NO_AVX512)
elseif(DAGOR_ARCH STREQUAL "x86_64")
elseif(DAGOR_ARCH STREQUAL "arm64")
  set(defines BLAKE3_USE_NEON)
endif()
dagor_add_target(NAME 3rdPartyLibs.hash.BLAKE3 STATIC LAX
  FILES_CMAKE BLAKE3_files.cmake
  INCLUDE_DIRECTORIES PRIVATE .
  COMPILE_DEFINITIONS PRIVATE ${defines}
)
