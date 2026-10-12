# Unit tests of the unit test harness itself (image compare, test environment, failures)
dagor_add_catch2_test(NAME unitTest-tests LAX
  TAGS engine
  FILES_CMAKE unitTest_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.ioSys engine.math engine.image
    engine.perfMon.daProfilerStub 3rdPartyLibs.eastl
)
