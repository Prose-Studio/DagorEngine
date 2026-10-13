# daProfiler API stub for programs without the profiler
# jam named the library engine/daProfilerStub.lib; dependents use the directory name
dagor_add_target(NAME engine.perfMon.daProfilerStub STATIC
  FILES_CMAKE daProfilerStub_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/perfMon ${DAGOR_PROG_DIR}/engine/perfMon/daProfiler
)
