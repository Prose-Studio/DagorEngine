dagor_add_target(NAME objLibCvt EXECUTABLE LAX
  OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/converters
  FILES_CMAKE objLib2Asset_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
    engine.lib3d engine.drv.drv3d_null engine.perfMon.daProfilerStub tools.libTools.staticGeom tools.libTools.dagFileRW
    tools.libTools.dtx tools.libTools.util
)
