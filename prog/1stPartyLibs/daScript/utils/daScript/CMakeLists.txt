# das: the daScript interpreter and test runner (dastest) of the engine, with its ECS and Dagor modules; installed into
# tools/util as das[-64]-<config> for the scripts that run it
if(WIN32 AND DAGOR_ARCH STREQUAL "x86_64")
  set(output_name das-64)
else()
  set(output_name das)
endif()

dagor_add_target(NAME das EXECUTABLE LAX OUTPUT_NAME ${output_name}
  FILES_CMAKE daScript_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  COMPILE_DEFINITIONS PRIVATE DAS_USE_BASE_CRASH_HANDLER=1
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.perfMon engine.memory.rtl engine.baseUtil engine.ioSys engine.startup
    engine.math 3rdPartyLibs.eastl 1stPartyLibs.daScript engine.daECS.core gameLibs.ecs.scripts.das
    gameLibs.dasModules.common engine.perfMon.daProfilerStub
  PROPERTIES DAGOR_DAS_CONSOLE ON DAGOR_NO_GPU ON
)
