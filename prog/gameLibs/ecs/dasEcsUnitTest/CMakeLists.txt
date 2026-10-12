# das_ecs_test: daECS + daScript; entity systems in tests/*.das react to EventStart/EventEnd broadcasts and record
# checks. The scripts are interpreted (the AOT build of this test belongs to the daScript AOT work of the game trees).
if(DAGOR_SANITIZE STREQUAL "none")
  set(memory "$<IF:$<CONFIG:Rel>,engine.memory.default.off,engine.memory.default.dbg>")
else()
  set(memory engine.memory.default.off)
endif()

dagor_add_executable(das_ecs_test defaultFileAccess.cpp unitModule.cpp unit_test.cpp dasModules/stub/aotstub.cpp)
target_include_directories(das_ecs_test PRIVATE . ${DAGOR_PROG_DIR}/engine/dagorInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include)
target_compile_definitions(das_ecs_test PRIVATE "DAS_ECS_TEST_ENGINE_ROOT=\"${DAGOR_ENGINE_ROOT}\"")
target_link_libraries(das_ecs_test PRIVATE Dagor::Quirrel ${memory} engine.osApiWrappers engine.kernel engine.perfMon
  engine.math engine.baseUtil engine.ioSys engine.startup engine.workCycle engine.daECS.core engine.daECS.io.datablock
  engine.daECS.utility gameLibs.ecs.scripts.das gameLibs.dasModules.common engine.daECS.gameResStub)
set_target_properties(das_ecs_test PROPERTIES DAGOR_NO_GPU ON)
dagor_add_exec_test(gameLibs.ecs.dasEcsUnitTest COMMAND $<TARGET_FILE:das_ecs_test> tests TAGS gameLibs ecs)
