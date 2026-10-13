# SEP client unit tests
if(WIN32)
  list(APPEND options /FC)
endif()

dagor_add_catch2_test(NAME sepClient-tests LAX
  TAGS gameLibs net
  FILES_CMAKE tests_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include ${DAGOR_PROG_DIR}/gameLibs/websocketJsonRpc/tests
    ${DAGOR_PROG_DIR}/gameLibs/sepClient/tests
  COMPILE_DEFINITIONS PRIVATE USE_EASTL
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE
    engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.ioSys engine.perfMon.daProfilerStub
    3rdPartyLibs.eastl gameLibs.sepClient gameLibs.websocketJsonRpc.tests.testHelpers
)
