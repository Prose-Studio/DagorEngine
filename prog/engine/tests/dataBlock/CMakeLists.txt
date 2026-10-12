# DataBlock (BLK) unit tests
dagor_add_catch2_test(NAME datablock-tests LAX
  TAGS engine
  FILES_CMAKE dataBlock_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.ioSys engine.math
    engine.perfMon.daProfilerStub 3rdPartyLibs.eastl
)
