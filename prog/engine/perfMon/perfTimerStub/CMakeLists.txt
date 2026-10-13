# Performance timer stubs
dagor_add_target(NAME engine.perfMon.perfTimerStub STATIC
  FILES_CMAKE perfTimerStub_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/engine/perfMon ${DAGOR_PROG_DIR}/engine/perfMon/daProfiler
)
