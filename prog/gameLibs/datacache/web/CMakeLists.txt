# Data cache: the web (HTTP) backend
set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(deps 3rdPartyLibs.eastl gameLibs.datacache.common gameLibs.datacache.file gameLibs.streamIO)
list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include)
list(APPEND deps 3rdPartyLibs.openssl-3.x)

dagor_add_target(NAME gameLibs.datacache.web STATIC
  FILES_CMAKE web_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE OPENSSL_SUPPRESS_DEPRECATED
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
