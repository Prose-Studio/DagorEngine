# Data cache: the web (HTTP) backend
dagor_add_target(NAME gameLibs.datacache.web STATIC
  FILES_CMAKE web_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include
  COMPILE_DEFINITIONS PRIVATE OPENSSL_SUPPRESS_DEPRECATED
  BUILD_DEPENDENCIES PRIVATE
    3rdPartyLibs.eastl gameLibs.datacache.common gameLibs.datacache.file gameLibs.streamIO 3rdPartyLibs.openssl-3.x
)
