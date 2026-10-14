# OpenSSL's MD5 alone (on the CPU detection of crypto/sha), for the libraries that hash without the rest of OpenSSL
include(../../openssl.cmake)
dagor_add_target(NAME 3rdPartyLibs.openssl-3.x.crypto.md5 STATIC LAX
  FILES_CMAKE md5_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${OPENSSL_INCLUDES}
  COMPILE_DEFINITIONS PRIVATE ${OPENSSL_C_DEFINES}
  COMPILE_OPTIONS PRIVATE "$<$<COMPILE_LANGUAGE:C>:${OPENSSL_C_OPTIONS}>"
  BUILD_DEPENDENCIES PUBLIC 3rdPartyLibs.openssl-3.x.crypto.sha
  LICENSES ${OPENSSL_DIR}/LICENSE.txt
)
