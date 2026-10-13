# Websocket client on libcurl
if(WIN32)
  list(APPEND options /FC)
endif()

dagor_add_target(NAME gameLibs.websocket STATIC
  FILES_CMAKE websocket_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/libb64/include ${DAGOR_PROG_DIR}/3rdPartyLibs/libcurl/include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include
  COMPILE_DEFINITIONS PRIVATE CURL_STATICLIB
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE
    3rdPartyLibs.eastl 3rdPartyLibs.libb64 3rdPartyLibs.hash engine.crypto 3rdPartyLibs.libcurl 3rdPartyLibs.openssl-3.x
)
