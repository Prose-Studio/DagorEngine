dagor_add_target(NAME gameLibs.ecs.game.actions STATIC
  FILES_CMAKE actions_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
