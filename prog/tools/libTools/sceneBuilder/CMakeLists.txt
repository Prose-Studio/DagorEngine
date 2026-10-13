dagor_add_target(NAME tools.libTools.sceneBuilder STATIC LAX
  FILES_CMAKE sceneBuilder_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
)
