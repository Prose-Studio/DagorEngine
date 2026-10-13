dagor_add_target(NAME dagCSG EXECUTABLE LAX OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/util/
  FILES_CMAKE dagCSG_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/math/carve/include
  COMPILE_DEFINITIONS PRIVATE NDEBUG CARVE_NODEBUG CARVE_USE_EXACT_PREDICATES
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.baseUtil engine.ioSys engine.math engine.lib3d
    engine.drv.drv3d_null engine.perfMon.daProfilerStub engine.startup tools.libTools.util tools.libTools.staticGeom
    tools.libTools.dagFileRW 3rdPartyLibs.math.carve
)
