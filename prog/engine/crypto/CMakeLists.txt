# Crypto helpers on OpenSSL (digests, ciphers, signatures). The programs that never encrypt set the DAGOR_NO_CRYPTO
# target property and get the stub, without OpenSSL; see dagor_add_link_choice().
dagor_add_target(NAME engine.crypto.standard STATIC
  FILES_CMAKE crypto_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include
  COMPILE_DEFINITIONS PRIVATE OPENSSL_IS_STATICALLY_LINKED
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.openssl-3.x
)
dagor_add_target(NAME engine.crypto.stub STATIC
  FILES_CMAKE stub_files.cmake
)
dagor_add_link_choice(engine.crypto PROPERTY DAGOR_NO_CRYPTO ON engine.crypto.stub OFF engine.crypto.standard)
