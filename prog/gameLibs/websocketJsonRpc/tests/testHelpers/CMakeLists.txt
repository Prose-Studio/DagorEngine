# Websocket JSON RPC test helpers (a local test server)
list(APPEND includes
  ${DAGOR_PROG_DIR}/3rdPartyLibs/catch2/src
  ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/websocketJsonRpc/tests
)
list(APPEND deps gameLibs.websocket gameLibs.websocketJsonRpc)
set(AllSrcFolder_CPP .)
dagor_glob_sources(sources DIRS ${AllSrcFolder_CPP} GLOB *.cpp)
if(WIN32)
  list(APPEND options /FC)
endif()

dagor_add_library(gameLibs.websocketJsonRpc.tests.testHelpers ${sources})
target_include_directories(gameLibs.websocketJsonRpc.tests.testHelpers PRIVATE ${includes})
target_compile_options(gameLibs.websocketJsonRpc.tests.testHelpers PRIVATE ${options})
target_link_libraries(gameLibs.websocketJsonRpc.tests.testHelpers PRIVATE ${deps})
