# The work cycle stub for programs without the engine's main loop (console tools on Linux). The perf variant: with the
# perf-timing stubs as well (WORKCYCLE_PERF_STUB) for benchmarks.
foreach(variant "" .perf)
  set(name engine.workCycle.stub${variant})
  dagor_add_target(NAME ${name} STATIC
    FILES_CMAKE stub_files.cmake
    INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/workCycle
  )
endforeach()
target_compile_definitions(engine.workCycle.stub.perf PRIVATE WORKCYCLE_PERF_STUB)
