# Performance monitoring stubs (misc counters, cache simulation) for programs without the profiler
set(includes ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/engine/perfMon)
set(sources misc.cpp cachesim.cpp)
set(deps engine.perfMon.daProfilerStub engine.perfMon.gpuProfilerStub engine.perfMon.perfTimerStub)

dagor_add_library(engine.perfMon.stub ${sources})
target_include_directories(engine.perfMon.stub PRIVATE ${includes})
target_link_libraries(engine.perfMon.stub PRIVATE ${deps})
