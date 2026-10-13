dagor_add_target(NAME DagOpt EXECUTABLE LAX
  OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/util/
  FILES_CMAKE DagOpt_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.baseUtil engine.ioSys engine.math engine.lib3d
    engine.drv.drv3d_null engine.perfMon.daProfilerStub engine.startup tools.libTools.util tools.libTools.staticGeom
    tools.libTools.dagFileRW tools.libTools.dtx
)
