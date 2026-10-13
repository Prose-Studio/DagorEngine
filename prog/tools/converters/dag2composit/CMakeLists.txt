dagor_add_target(NAME dag2composit EXECUTABLE LAX
  OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/util
  FILES_CMAKE dag2composit_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
    engine.lib3d engine.drv.drv3d_null engine.perfMon.daProfilerStub tools.libTools.util tools.libTools.dagFileRW
)
