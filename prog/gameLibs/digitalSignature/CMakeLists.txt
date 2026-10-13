# Digital signature creation and checking on OpenSSL

dagor_add_target(NAME gameLibs.digitalSignature STATIC LAX
  FILES_CMAKE digitalSignature_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include
)
