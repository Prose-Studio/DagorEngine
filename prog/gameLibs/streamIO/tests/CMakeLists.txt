# HTTP streaming unit tests (against a local HTTP server)
dagor_add_catch2_test(NAME streamIO-tests LAX
  TAGS gameLibs net REQUIRES http_server
  FILES_CMAKE tests_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.ioSys engine.math engine.coreUtil
    engine.startup engine.perfMon.daProfilerStub gameLibs.streamIO
)
