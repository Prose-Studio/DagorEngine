# Touchpad gesture recognition unit tests
dagor_add_catch2_test(NAME touchpadGestures-tests LAX
  TAGS engine
  FILES_CMAKE touchpadGestures_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.ioSys engine.math engine.perfMon.daProfilerStub
    3rdPartyLibs.eastl
)
