set(FILES blake3.c blake3_dispatch.c blake3_portable.c)
if(NOT DAGOR_ARCH STREQUAL "e2k" AND DAGOR_ARCH STREQUAL "x86_64" AND WIN32)
  list(APPEND FILES blake3_sse2_x86-64_windows_msvc.masm blake3_sse41_x86-64_windows_msvc.masm
    blake3_avx2_x86-64_windows_msvc.masm)
elseif(DAGOR_ARCH STREQUAL "x86_64")
  list(APPEND FILES blake3_avx2_x86-64_unix.S blake3_avx512_x86-64_unix.S blake3_sse2_x86-64_unix.S
    blake3_sse41_x86-64_unix.S)
elseif(DAGOR_ARCH STREQUAL "arm64")
  list(APPEND FILES blake3_neon.c)
endif()
