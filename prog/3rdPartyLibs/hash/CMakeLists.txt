# sha1/sha256/sha3/md5/xxhash/crc32/rijndael; the SHA-2 implementation comes from OpenSSL's sha module
add_subdirectory(BLAKE3)

set(sources
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
set(c_options)
if(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  # warning 6386: Buffer overrun: accessing 'argument 1', the writable size is '64' bytes, but '746' bytes might be written
  list(APPEND c_options /wd6386)
elseif((MSVC AND CMAKE_CXX_COMPILER_ID STREQUAL "Clang") AND DAGOR_ARCH STREQUAL "x86_64")
  set_property(SOURCE crc32c.c APPEND PROPERTY COMPILE_OPTIONS -mcrc32)
endif()
set(options)
if(DAGOR_ARCH STREQUAL "e2k")
  list(APPEND options -Wno-reduced-alignment)
endif()

dagor_add_library(3rdPartyLibs.hash LAX ${sources})
target_include_directories(3rdPartyLibs.hash PRIVATE . SHA3IUF ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include)
target_compile_definitions(3rdPartyLibs.hash PRIVATE OPENSSL_SUPPRESS_DEPRECATED)
target_compile_options(3rdPartyLibs.hash PRIVATE ${options})
target_compile_options(3rdPartyLibs.hash PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>")
target_link_libraries(3rdPartyLibs.hash PRIVATE 3rdPartyLibs.openssl-3.x.crypto.sha)
