# daProfiler API stub for programs without the profiler
set(includes
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/engine/perfMon
  ${DAGOR_PROG_DIR}/engine/perfMon/daProfiler
)
set(sources daProfilerStub.cpp)

# jam named the library engine/daProfilerStub.lib; dependents use the directory name
dagor_add_library(engine.perfMon.daProfilerStub ${sources})
target_include_directories(engine.perfMon.daProfilerStub PRIVATE ${includes})
