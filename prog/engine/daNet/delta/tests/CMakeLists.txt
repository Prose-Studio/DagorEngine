# daNet delta compression unit tests
dagor_add_catch2_test(NAME netdelta-tests LAX
  TAGS engine net
  FILES_CMAKE tests_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.ioSys engine.math
    engine.perfMon.daProfilerStub engine.daNet.delta
)
