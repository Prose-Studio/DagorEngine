# Low latency mode (NVIDIA Reflex / AMD Anti-Lag) with its debug renderer, for the programs that set the
# DAGOR_LOW_LATENCY target property; a stub in the others (see dagor_add_link_choice())
set(includes ${DAGOR_PROG_DIR}/engine/sharedInclude)
dagor_add_target(NAME engine.lowLatency.framework STATIC LAX
  FILES_CMAKE framework_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  BUILD_DEPENDENCIES PRIVATE engine.profilerTracker
)
dagor_add_target(NAME engine.lowLatency.stub STATIC LAX
  FILES_CMAKE stub_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  BUILD_DEPENDENCIES PRIVATE engine.profilerTracker
)
dagor_add_link_choice(engine.lowLatency PROPERTY DAGOR_LOW_LATENCY
  ON engine.lowLatency.framework OFF engine.lowLatency.stub)
