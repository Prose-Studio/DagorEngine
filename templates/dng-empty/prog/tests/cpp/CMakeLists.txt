# C++ unit tests of the game (Catch2, see <engine>/_docs/source/testing/cpp_unit_tests.md)
dagor_add_catch2_test(dng_empty-tests TAGS dng_empty LAX main.cpp test_config.cpp)
target_link_libraries(dng_empty-tests PRIVATE engine.memory engine.kernel engine.osApiWrappers engine.baseUtil
  engine.ioSys engine.math engine.perfMon.daProfilerStub 3rdPartyLibs.eastl)
