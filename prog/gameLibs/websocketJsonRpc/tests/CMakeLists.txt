# Websocket JSON RPC unit tests
add_subdirectory(testHelpers)

set(AllSrcFolder_CPP . wsJsonRpcConnection wsJsonRpcPersistentConnection)
dagor_glob_sources(sources DIRS ${AllSrcFolder_CPP} GLOB *.cpp)
list(APPEND includes
  ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/websocketJsonRpc/tests
)
list(APPEND defines USE_EASTL)
if(WIN32)
  list(APPEND options /FC)
endif()
list(APPEND deps engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.ioSys
  engine.perfMon.daProfilerStub 3rdPartyLibs.eastl gameLibs.websocketJsonRpc gameLibs.websocketJsonRpc.tests.testHelpers)

dagor_add_catch2_test(websocketJsonRpc-tests TAGS gameLibs net LAX ${sources})
target_include_directories(websocketJsonRpc-tests PRIVATE ${includes})
target_compile_definitions(websocketJsonRpc-tests PRIVATE ${defines})
target_compile_options(websocketJsonRpc-tests PRIVATE ${options})
target_link_libraries(websocketJsonRpc-tests PRIVATE ${deps})
