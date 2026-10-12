# daNet unit tests
dagor_add_catch2_test(NAME danet-tests LAX
  TAGS engine net
  FILES_CMAKE tests_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.ioSys engine.math
    engine.perfMon.daProfilerStub 3rdPartyLibs.eastl engine.daNet
)
