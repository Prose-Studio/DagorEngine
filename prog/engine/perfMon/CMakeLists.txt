# Performance monitoring: profiler modes and settings, statistics, memory reports, platform events, the GPU profiler.
# Programs without a 3d driver set the DAGOR_NO_GPU target property: they get the GPU profiler stub
# (engine/perfMon/gpuProfilerStub) instead of gpuProfiler.cpp, see dagor_add_link_choice().
set(includes ${DAGOR_PROG_DIR}/engine/perfMon)
dagor_add_target(NAME engine.perfMon.gpuProfiler STATIC
  FILES_CMAKE gpuProfiler_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
)
dagor_add_link_choice(engine.perfMon.gpu PROPERTY DAGOR_NO_GPU
  ON engine.perfMon.gpuProfilerStub OFF engine.perfMon.gpuProfiler)

set(deps engine.perfMon.gpu)
if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  list(APPEND deps engine.perfMon.daProfiler)
endif()
dagor_add_target(NAME engine.perfMon STATIC
  FILES_CMAKE perfMon_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
