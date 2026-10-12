# The work cycle: the main loop, timing, input device init, the console in Dev and Dbg
set(deps engine.perfMon engine.lowLatency engine.coreUtil)
list(APPEND deps "$<$<CONFIG:Dev,Dbg>:engine.consoleProc>")
list(APPEND deps engine.drv.vr_device)

dagor_add_target(NAME engine.workCycle STATIC
  FILES_CMAKE workCycle_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
