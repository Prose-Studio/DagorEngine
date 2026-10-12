# GPU profiler stub for programs without a 3d driver
dagor_add_target(NAME engine.perfMon.gpuProfilerStub STATIC
  FILES_CMAKE gpuProfilerStub_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/engine/perfMon ${DAGOR_PROG_DIR}/engine/perfMon/daProfiler
)
