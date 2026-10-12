# Asynchronous HTTP client on libcurl
list(APPEND includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
list(APPEND deps 3rdPartyLibs.eastl)
list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/libcurl/include)
list(APPEND deps 3rdPartyLibs.libcurl)

dagor_add_target(NAME gameLibs.asyncHTTPClient STATIC
  FILES_CMAKE asyncHTTPClient_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE CURL_STATICLIB
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
