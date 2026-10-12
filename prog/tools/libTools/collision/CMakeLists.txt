# Collision export helpers: export node types by name, V-HACD mesh face checks and fixes
dagor_add_target(NAME tools.libTools.collision STATIC LAX
  FILES_CMAKE collision_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sharedInclude
)
