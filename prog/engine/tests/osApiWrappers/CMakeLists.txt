# OS API wrapper unit tests (named mounts)
dagor_add_catch2_test(NAME osApiWrappers-tests LAX
  TAGS engine
  FILES_CMAKE osApiWrappers_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.ioSys engine.math
    engine.perfMon.daProfilerStub 3rdPartyLibs.eastl
)
