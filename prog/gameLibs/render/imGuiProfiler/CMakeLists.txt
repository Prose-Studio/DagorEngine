# The ImGui profiler window: CPU and GPU timings of the profiler's events, with draw stats
add_subdirectory(stub)

dagor_add_target(NAME gameLibs.render.imGuiProfiler STATIC
  FILES_CMAKE imGuiProfiler_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
