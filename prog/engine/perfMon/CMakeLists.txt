# Performance monitoring: profiler modes and settings, statistics, memory reports, platform events, the GPU profiler.
# Programs without a 3d driver set the DAGOR_NO_GPU target property: they get the GPU profiler stub
# (engine/perfMon/gpuProfilerStub) instead of gpuProfiler.cpp, see dagor_add_link_choice().
add_subdirectory(daProfiler)
add_subdirectory(daProfilerStub)
add_subdirectory(gpuProfilerStub)
add_subdirectory(perfTimerStub)
add_subdirectory(stub)

set(sources
  profilerModes.cpp
  profilerSettings.cpp
  stat3d.cpp
  tdrProfile.cpp
  statStd.cpp
  perfMonStat.cpp
  platformEvents.cpp
  sleepPrecise.cpp
  memoryReport.cpp
  memoryReportVramQuery.cpp
  memoryReportLog.cpp
  stub/cachesim.cpp
  "$<$<NOT:$<CONFIG:Rel>>:${CMAKE_CURRENT_SOURCE_DIR}/alternateProfiler.cpp>"
)
set(includes ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/engine/perfMon)

dagor_add_library(engine.perfMon.gpuProfiler gpuProfiler.cpp)
target_include_directories(engine.perfMon.gpuProfiler PRIVATE ${includes})
dagor_add_link_choice(engine.perfMon.gpu PROPERTY DAGOR_NO_GPU
  ON engine.perfMon.gpuProfilerStub OFF engine.perfMon.gpuProfiler)

set(deps engine.perfMon.gpu)
if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  list(APPEND deps engine.perfMon.daProfiler)
endif()
dagor_add_library(engine.perfMon ${sources})
target_include_directories(engine.perfMon PRIVATE ${includes})
target_link_libraries(engine.perfMon PRIVATE ${deps})
