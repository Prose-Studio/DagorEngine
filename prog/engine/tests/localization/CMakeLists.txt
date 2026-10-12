# Localization table unit tests
dagor_add_catch2_test(NAME localization-tests LAX
  TAGS engine
  FILES_CMAKE localization_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.coreUtil engine.ioSys engine.math
    engine.perfMon.daProfilerStub 3rdPartyLibs.eastl
)
