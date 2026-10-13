dagor_add_target(NAME mat_analyser EXECUTABLE LAX
  FILES_CMAKE dagMatAnalyser_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/engine/shaders ${DAGOR_PROG_DIR}/engine/sharedInclude
  COMPILE_DEFINITIONS PRIVATE SET_DEFAULT_MAX_SHVARS=8192
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
    engine.perfMon.daProfilerStub engine.lib3d engine.drv.drv3d_null engine.shaders tools.libTools.util
    tools.libTools.dagFileRW 3rdPartyLibs.eastl System::d3dcompiler
  PROPERTIES DAGOR_EXCEPTIONS ON
  CDK
)
