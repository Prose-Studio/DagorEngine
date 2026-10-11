# C++ unit tests of the game (Catch2, see <engine>/_docs/source/testing/cpp_unit_tests.md)
dagor_add_catch2_test(dng_empty-tests TAGS dng_empty
  SOURCES
    main.cpp
    test_config.cpp
  DEPS
    engine/memory
    engine/kernel
    engine/osApiWrappers
    engine/baseUtil
    engine/ioSys
    engine/math
    engine/perfMon/daProfilerStub
    3rdPartyLibs/eastl
)
