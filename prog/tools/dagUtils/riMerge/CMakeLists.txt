dagor_add_target(NAME riMerge EXECUTABLE LAX OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/util
  FILES_CMAKE riMerge_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.baseUtil engine.ioSys engine.math engine.lib3d
    engine.startup engine.perfMon.daProfilerStub engine.drv.drv3d_null tools.libTools.util tools.libTools.staticGeom
    tools.libTools.dagFileRW tools.libTools.dtx
)
