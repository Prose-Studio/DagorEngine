# The work cycle: the main loop, timing, input device init, the console in Dev and Dbg
dagor_add_target(NAME engine.workCycle STATIC
  FILES_CMAKE workCycle_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.perfMon engine.lowLatency engine.coreUtil "$<$<CONFIG:Dev,Dbg>:engine.consoleProc>" engine.drv.vr_device
)
