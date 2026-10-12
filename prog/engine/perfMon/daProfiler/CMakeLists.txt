# daProfiler: the engine's CPU/GPU profiler with its capture and dump formats
set(includes ${DAGOR_PROG_DIR}/engine/perfMon/daProfiler ${DAGOR_PROG_DIR}/engine/sharedInclude)
if(ANDROID)
  list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/libunwind/include)
  list(APPEND deps 3rdPartyLibs.libunwind)
endif()

dagor_add_target(NAME engine.perfMon.daProfiler STATIC
  FILES_CMAKE daProfiler_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE __B_KERNEL_LIB
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
