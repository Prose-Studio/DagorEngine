set(FILES
  sha1.cpp
  sha256.cpp
  sha3.cpp
  md5.c
  xxhash.c
  crc32.c
  crc32c.c
  rijndael-alg-fst.c
  rijndael-api-fst.c
  xxh_x86dispatch_auto.c
  SHA3IUF/sha3.c
)
if(NOT CMAKE_CXX_COMPILER_ID STREQUAL "MSVC" AND (MSVC AND CMAKE_CXX_COMPILER_ID STREQUAL "Clang") AND DAGOR_ARCH
  STREQUAL "x86_64")
  set_property(SOURCE crc32c.c APPEND PROPERTY COMPILE_OPTIONS -mcrc32)
endif()
