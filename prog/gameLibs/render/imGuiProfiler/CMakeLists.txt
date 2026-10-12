# The ImGui profiler window: CPU and GPU timings of the profiler's events, with draw stats
add_subdirectory(stub)

set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources imGuiProfiler.cpp)

dagor_add_library(gameLibs.render.imGuiProfiler ${sources})
target_include_directories(gameLibs.render.imGuiProfiler PRIVATE ${includes})
