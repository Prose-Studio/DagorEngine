dagor_add_target(NAME dag2blk EXECUTABLE LAX OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/converters/dag2blk
  FILES_CMAKE dag2blk_files.cmake
  COMPILE_DEFINITIONS PRIVATE __B_MAIN
  BUILD_DEPENDENCIES PRIVATE
    tools.libTools.dagFileRW tools.libTools.util engine.osApiWrappers engine.kernel engine.memory engine.ioSys
    engine.startup engine.baseUtil engine.math engine.image engine.lib3d engine.drv.drv3d_null
    engine.perfMon.daProfilerStub
)
