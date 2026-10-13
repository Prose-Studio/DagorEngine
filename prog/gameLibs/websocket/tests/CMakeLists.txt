# WebSocket client unit tests (against the bundled libcurl)
set(options)
if(WIN32)
  set(options /FC)
endif()
dagor_add_catch2_test(NAME websocket-tests LAX
  TAGS gameLibs net
  FILES_CMAKE tests_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/websocket ${DAGOR_PROG_DIR}/3rdPartyLibs/libcurl/include
  COMPILE_DEFINITIONS PRIVATE USE_EASTL CURL_STATICLIB WEBSOCKET_TESTS_BUNDLED_CURL=1
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE
    engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.ioSys engine.perfMon.daProfilerStub
    3rdPartyLibs.eastl gameLibs.websocket
)
