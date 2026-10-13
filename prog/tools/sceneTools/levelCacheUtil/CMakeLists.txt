dagor_add_target(NAME levelCacheUtil EXECUTABLE LAX
  FILES_CMAKE levelCacheUtil_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
    engine.perfMon.daProfilerStub tools.libTools.util tools.libTools.dtx
  CDK
)
