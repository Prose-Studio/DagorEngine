# A benchmark of Quirrel's ECS-computed values (ecsFrpBench), next to its sources as jam built it
dagor_add_target(NAME ecsFrpBench EXECUTABLE NO_CONFIG_POSTFIX
  OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  FILES_CMAKE bench_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel ${DAGOR_PROG_DIR}/gameLibs
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.coreUtil
    engine.math engine.perfMon.daProfilerStub engine.consoleProc engine.workCycle engine.lib3d engine.drv.drv3d_stub
    engine.daECS.core engine.daECS.io.datablock engine.daECS.utility engine.daECS.gameResStub gameLibs.quirrel.frp
    gameLibs.quirrel.ecsComputed gameLibs.ecs.scripts.sq gameLibs.quirrel.quirrel_json 3rdPartyLibs.eastl Dagor::Quirrel
)
