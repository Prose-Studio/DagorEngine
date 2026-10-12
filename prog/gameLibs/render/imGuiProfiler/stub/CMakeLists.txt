# ImGui profiler window stub for programs without it
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources imGuiProfilerStub.cpp)

dagor_add_library(gameLibs.render.imGuiProfiler.stub ${sources})
target_include_directories(gameLibs.render.imGuiProfiler.stub PRIVATE ${includes})
