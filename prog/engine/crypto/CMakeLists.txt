# Crypto helpers on OpenSSL (digests, ciphers, signatures)
dagor_add_target(NAME engine.crypto STATIC
  FILES_CMAKE crypto_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include
  COMPILE_DEFINITIONS PRIVATE OPENSSL_IS_STATICALLY_LINKED
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.openssl-3.x
)
