# SEP client unit tests
set(AllSrcFolder_CPP . sepTestHelpers)
dagor_glob_sources(sources DIRS ${AllSrcFolder_CPP} GLOB *.cpp)
list(APPEND includes
  ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/websocketJsonRpc/tests
  ${DAGOR_PROG_DIR}/gameLibs/sepClient/tests
)
list(APPEND defines USE_EASTL)
if(WIN32)
  list(APPEND options /FC)
endif()
list(APPEND deps engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.ioSys
  engine.perfMon.daProfilerStub 3rdPartyLibs.eastl gameLibs.sepClient gameLibs.websocketJsonRpc.tests.testHelpers)

dagor_add_catch2_test(sepClient-tests TAGS gameLibs net LAX ${sources})
target_include_directories(sepClient-tests PRIVATE ${includes})
target_compile_definitions(sepClient-tests PRIVATE ${defines})
target_compile_options(sepClient-tests PRIVATE ${options})
target_link_libraries(sepClient-tests PRIVATE ${deps})
