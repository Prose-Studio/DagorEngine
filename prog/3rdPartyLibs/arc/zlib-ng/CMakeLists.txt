# zlib-ng in zlib-compatible mode, with the SIMD paths of the target
set(AllAVX2Sources slide_hash_avx2.c chunkset_avx.c compare256_avx2.c adler32_avx2.c)
set(AllACLESources crc32_acle.c insert_string_acle.c)
list(APPEND c_options -DZLIB_COMPAT)
if(CMAKE_SYSTEM_NAME MATCHES "^(Linux|Windows)$")
  if(DAGOR_ARCH STREQUAL "x86_64")
    list(APPEND c_options -DX86_FEATURES -DX86_SSE2 -DX86_SSE2_CHUNKSET -DX86_SSE2_SLIDEHASH)
  elseif(DAGOR_ARCH STREQUAL "arm64")
    list(APPEND c_options
      -DARM_FEATURES
      -DARM_NEON_SLIDEHASH
      -DARM_NEON_CHUNKSET
      -DARM_NEON_ADLER32
      -DARM_NEON_HASLD4
    )
  endif()
  if(WIN32 AND DAGOR_ARCH STREQUAL "x86_64")
    list(APPEND c_options -wd4267)
  endif()
elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  if(DAGOR_ARCH STREQUAL "x86_64")
    list(APPEND c_options -DX86_FEATURES -DX86_SSE2 -DX86_SSE2_CHUNKSET -DX86_SSE2_SLIDEHASH)
  elseif(DAGOR_ARCH STREQUAL "arm64")
    list(APPEND c_options
      -DARM_FEATURES
      -DARM_NEON_SLIDEHASH
      -DARM_NEON_CHUNKSET
      -DARM_NEON_ADLER32
      -DARM_NEON_HASLD4
    )
  endif()
endif()
if(DAGOR_ARCH MATCHES "^(e2k|x86_64)$")
  list(APPEND c_options -DX86_SSSE3)
endif()
if(CMAKE_SYSTEM_NAME MATCHES "^(Android|iOS)$")
  list(APPEND c_options
    -DARM_FEATURES
    -DARM_NEON_SLIDEHASH
    -DARM_NEON_CHUNKSET
    -DARM_NEON_ADLER32
    -DARM_NEON_HASLD4
  )
endif()

dagor_add_target(NAME 3rdPartyLibs.arc.zlib-ng STATIC LAX
  FILES_CMAKE zlib-ng_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zlib-ng
  COMPILE_OPTIONS PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
  FORCE_INCLUDES supp/dag_null.h
)
