# Asynchronous HTTP client on libcurl
dagor_add_target(NAME gameLibs.asyncHTTPClient STATIC
  FILES_CMAKE asyncHTTPClient_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/libcurl/include
  COMPILE_DEFINITIONS PRIVATE CURL_STATICLIB
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl 3rdPartyLibs.libcurl
)
