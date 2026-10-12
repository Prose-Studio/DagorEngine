set(FILES
  adler32.c
  chunkset.c
  compare256.c
  compress.c
  cpu_features.c
  crc32.c
  crc32_comb.c
  crc32_fold.c
  deflate.c
  deflate_fast.c
  deflate_huff.c
  deflate_medium.c
  deflate_quick.c
  deflate_rle.c
  deflate_slow.c
  deflate_stored.c
  functable.c
  gzlib.c
  gzread.c
  gzwrite.c
  infback.c
  inffast.c
  inflate.c
  inftrees.c
  insert_string.c
  insert_string_roll.c
  slide_hash.c
  trees.c
  uncompr.c
  zutil.c
)
set(Allx86Sources
  adler32_ssse3.c
  chunkset_sse2.c
  compare256_sse2.c
  crc32_fold_pclmulqdq.c
  crc32_fold_vpclmulqdq.c
  insert_string_sse42.c
  slide_hash_sse2.c
  x86_features.c
)
set(AllNEONSources adler32_neon.c arm_features.c chunkset_neon.c slide_hash_neon.c)
set(MacX86Sources chunkset_sse2.c compare256_sse2.c slide_hash_sse2.c x86_features.c)
if(CMAKE_SYSTEM_NAME MATCHES "^(Linux|Windows)$")
  if(DAGOR_ARCH STREQUAL "x86_64")
    set(_Allx86Sources_1 ${Allx86Sources})
    list(TRANSFORM _Allx86Sources_1 PREPEND "arch/x86/")
    list(APPEND FILES ${_Allx86Sources_1})
  elseif(DAGOR_ARCH STREQUAL "arm64")
    set(_AllNEONSources_2 ${AllNEONSources})
    list(TRANSFORM _AllNEONSources_2 PREPEND "arch/arm/")
    list(APPEND FILES ${_AllNEONSources_2})
  endif()
elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  if(DAGOR_ARCH STREQUAL "x86_64")
    set(_MacX86Sources_3 ${MacX86Sources})
    list(TRANSFORM _MacX86Sources_3 PREPEND "arch/x86/")
    list(APPEND FILES ${_MacX86Sources_3})
  elseif(DAGOR_ARCH STREQUAL "arm64")
    set(_AllNEONSources_4 ${AllNEONSources})
    list(TRANSFORM _AllNEONSources_4 PREPEND "arch/arm/")
    list(APPEND FILES ${_AllNEONSources_4})
  endif()
endif()
if(CMAKE_SYSTEM_NAME MATCHES "^(Android|iOS)$")
  set(_AllNEONSources_5 ${AllNEONSources})
  list(TRANSFORM _AllNEONSources_5 PREPEND "arch/arm/")
  list(APPEND FILES ${_AllNEONSources_5})
endif()
