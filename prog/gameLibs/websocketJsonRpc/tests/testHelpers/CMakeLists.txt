# Websocket JSON RPC test helpers (a local test server)
if(WIN32)
  list(APPEND options /FC)
endif()

dagor_add_target(NAME gameLibs.websocketJsonRpc.tests.testHelpers STATIC
  FILES_CMAKE testHelpers_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/catch2/src ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/websocketJsonRpc/tests
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE gameLibs.websocket gameLibs.websocketJsonRpc
)
