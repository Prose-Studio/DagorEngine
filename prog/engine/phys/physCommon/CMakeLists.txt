# Physics resources (bodies and helpers), physics counters and twist controllers, common to the physics libraries
dagor_add_target(NAME engine.phys.physCommon STATIC LAX
  FILES_CMAKE physCommon_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
)
