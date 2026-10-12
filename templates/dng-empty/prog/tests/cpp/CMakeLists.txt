# C++ unit tests of the game (Catch2, see <engine>/_docs/source/testing/cpp_unit_tests.md)
dagor_add_catch2_test(NAME dng_empty-tests LAX
  TAGS dng_empty
  FILES_CMAKE cpp_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.ioSys engine.math
    engine.perfMon.daProfilerStub 3rdPartyLibs.eastl
)
