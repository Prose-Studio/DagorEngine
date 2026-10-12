# Performance timer stubs
set(includes
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/engine/perfMon
  ${DAGOR_PROG_DIR}/engine/perfMon/daProfiler
)
set(sources perfTimerStub.cpp)

dagor_add_library(engine.perfMon.perfTimerStub ${sources})
target_include_directories(engine.perfMon.perfTimerStub PRIVATE ${includes})
