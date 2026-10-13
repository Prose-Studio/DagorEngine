# SEP client: JSON RPC over websockets with hostname resolution through c-ares
if(WIN32)
  list(APPEND options /FC)
endif()

dagor_add_target(NAME gameLibs.sepClient STATIC
  FILES_CMAKE sepClient_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include ${DAGOR_PROG_DIR}/3rdPartyLibs/c-ares
  COMPILE_DEFINITIONS PRIVATE SEPCLIENT_USE_CARES CARES_STATICLIB
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE gameLibs.websocketJsonRpc 3rdPartyLibs.c-ares
)
