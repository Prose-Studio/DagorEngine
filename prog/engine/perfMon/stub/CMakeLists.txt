# Performance monitoring stubs (misc counters, cache simulation) for programs without the profiler
dagor_add_target(NAME engine.perfMon.stub STATIC
  FILES_CMAKE stub_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/engine/perfMon
  BUILD_DEPENDENCIES PRIVATE engine.perfMon.daProfilerStub engine.perfMon.gpuProfilerStub engine.perfMon.perfTimerStub
)
