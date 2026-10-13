dagor_add_target(NAME dag2obGroups EXECUTABLE LAX OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/util
  FILES_CMAKE dag2objectGroups_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
    engine.drv.drv3d_null engine.lib3d engine.shaders engine.image engine.ioSys engine.perfMon.daProfilerStub
    tools.libTools.util tools.libTools.dagFileRW tools.libTools.staticGeom tools.libTools.dtx 3rdPartyLibs.image.psdRead
)
