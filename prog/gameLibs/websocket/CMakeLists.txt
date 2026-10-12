# Websocket client on libcurl
list(APPEND includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/libb64/include)
list(APPEND deps 3rdPartyLibs.eastl 3rdPartyLibs.libb64 3rdPartyLibs.hash engine.crypto)
list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/libcurl/include)
list(APPEND deps 3rdPartyLibs.libcurl)
if(WIN32)
  list(APPEND options /FC)
endif()
list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include)
list(APPEND deps 3rdPartyLibs.openssl-3.x)

dagor_add_target(NAME gameLibs.websocket STATIC
  FILES_CMAKE websocket_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE CURL_STATICLIB
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
