dagor_add_target(NAME res2AssetCvt EXECUTABLE LAX
  OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/converters
  FILES_CMAKE res2Asset_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
    engine.lib3d engine.perfMon.daProfilerStub tools.libTools.util tools.libTools.dagFileRW tools.libTools.staticGeom
)
