# GPU profiler stub for programs without a 3d driver
set(includes
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/engine/perfMon
  ${DAGOR_PROG_DIR}/engine/perfMon/daProfiler
)
set(sources gpuProfilerStub.cpp)

dagor_add_library(engine.perfMon.gpuProfilerStub ${sources})
target_include_directories(engine.perfMon.gpuProfilerStub PRIVATE ${includes})
