# SEP client: JSON RPC over websockets with hostname resolution through c-ares
if(DAGOR_ENGINE_TESTS)
  add_subdirectory(tests)
endif()

list(APPEND includes
  ${DAGOR_PROG_DIR}/dagorInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
)
list(APPEND deps gameLibs.websocketJsonRpc)
list(APPEND deps 3rdPartyLibs.c-ares)
list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/c-ares)
if(WIN32)
  list(APPEND options /FC)
endif()

dagor_add_target(NAME gameLibs.sepClient STATIC
  FILES_CMAKE sepClient_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE SEPCLIENT_USE_CARES CARES_STATICLIB
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
