dagor_add_target(NAME texren EXECUTABLE LAX
  OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/util
  FILES_CMAKE DagTexRename_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
    engine.lib3d engine.perfMon.daProfilerStub engine.drv.drv3d_null tools.libTools.util tools.libTools.dagFileRW
)
