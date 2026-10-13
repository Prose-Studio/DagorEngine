dagor_add_target(NAME hdrFind EXECUTABLE LAX OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/util
  FILES_CMAKE hdr_analyze_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
    engine.lib3d engine.perfMon.daProfilerStub engine.drv.drv3d_null tools.libTools.dagFileRW
)
