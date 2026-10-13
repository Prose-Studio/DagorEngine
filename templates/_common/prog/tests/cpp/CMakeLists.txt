# C++ unit tests of the game (Catch2, see <engine>/_docs/source/testing/cpp_unit_tests.md)
dagor_add_catch2_test(NAME starter_game-tests LAX
  TAGS starter_game
  FILES_CMAKE cpp_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.ioSys engine.math
    engine.perfMon.daProfilerStub 3rdPartyLibs.eastl
)
