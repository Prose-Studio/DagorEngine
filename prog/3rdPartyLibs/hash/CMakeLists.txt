# sha1/sha256/sha3/md5/xxhash/crc32/rijndael; the SHA-2 implementation comes from OpenSSL's sha module
set(c_options)
if(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  # warning 6386: Buffer overrun: accessing 'argument 1', the writable size is '64' bytes, but '746' bytes might be written
  list(APPEND c_options /wd6386)
endif()
set(options)
if(DAGOR_ARCH STREQUAL "e2k")
  list(APPEND options -Wno-reduced-alignment)
endif()

dagor_add_target(NAME 3rdPartyLibs.hash STATIC LAX
  FILES_CMAKE hash_files.cmake
  INCLUDE_DIRECTORIES PRIVATE . SHA3IUF ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include
  COMPILE_DEFINITIONS PRIVATE OPENSSL_SUPPRESS_DEPRECATED
  COMPILE_OPTIONS PRIVATE ${options} "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.openssl-3.x.crypto.sha
)
