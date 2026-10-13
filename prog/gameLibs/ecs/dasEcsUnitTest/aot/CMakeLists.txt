# The daScript AOT compiler of the daECS unit tests (tools/util; the system allocator)
dagor_add_target(NAME das_ecs_test-aot EXECUTABLE LAX
  OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/util
  FILES_CMAKE aot_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/ecs/dasEcsUnitTest ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.perfMon engine.math engine.gameRes engine.memory.rtl engine.consoleProc
    engine.drv.drv3d_null engine.baseUtil engine.startup engine.workCycle 3rdPartyLibs.eastl 1stPartyLibs.daScript
    1stPartyLibs.daScriptModules.rapidjson engine.daECS.core engine.daECS.gameResStub engine.daECS.io.datablock
    engine.daECS.utility gameLibs.ecs.scripts.das gameLibs.ecs.scripts.sq gameLibs.dasModules.common
    gameLibs.quirrel.bindQuirrelEx Dagor::Quirrel
  PROPERTIES DAGOR_NO_GPU ON
)
