# das_ecs_test: daECS + daScript; entity systems in tests/*.das react to EventStart/EventEnd broadcasts and record
# checks. The scripts are interpreted (the AOT build of this test belongs to the daScript AOT work of the game trees).
if(DAGOR_SANITIZE STREQUAL "none")
  set(memory "$<IF:$<CONFIG:Rel>,engine.memory.default.off,engine.memory.default.dbg>")
else()
  set(memory engine.memory.default.off)
endif()

dagor_add_target(NAME das_ecs_test EXECUTABLE
  FILES_CMAKE dasEcsUnitTest_files.cmake
  INCLUDE_DIRECTORIES PRIVATE . ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  COMPILE_DEFINITIONS PRIVATE "DAS_ECS_TEST_ENGINE_ROOT=\"${DAGOR_ENGINE_ROOT}\""
  BUILD_DEPENDENCIES PRIVATE
    Dagor::Quirrel ${memory} engine.osApiWrappers engine.kernel engine.perfMon engine.math engine.baseUtil engine.ioSys
    engine.startup engine.workCycle engine.daECS.core engine.daECS.io.datablock engine.daECS.utility
    gameLibs.ecs.scripts.das gameLibs.dasModules.common engine.daECS.gameResStub
  PROPERTIES DAGOR_NO_GPU ON
)
dagor_add_exec_test(gameLibs.ecs.dasEcsUnitTest COMMAND $<TARGET_FILE:das_ecs_test> tests TAGS gameLibs ecs)
