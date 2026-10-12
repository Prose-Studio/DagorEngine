# Digital signature creation and checking on OpenSSL
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include)

dagor_add_target(NAME gameLibs.digitalSignature STATIC LAX
  FILES_CMAKE digitalSignature_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
)
