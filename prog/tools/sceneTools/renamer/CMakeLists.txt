dagor_add_target(NAME renamer EXECUTABLE LAX
  FILES_CMAKE renamer_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
    engine.perfMon.daProfilerStub gameLibs.gameResPatcher tools.libTools.util
  CDK
)
