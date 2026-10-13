# Force feedback (rumble scaling) unit tests
dagor_add_catch2_test(NAME forceFeedback-tests
  TAGS gameLibs
  FILES_CMAKE tests_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.ioSys engine.math engine.startup
    engine.perfMon.daProfilerStub gameLibs.forceFeedback 3rdPartyLibs.eastl
)
