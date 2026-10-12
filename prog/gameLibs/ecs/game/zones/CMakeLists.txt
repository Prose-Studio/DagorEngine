dagor_add_target(NAME gameLibs.ecs.game.zones STATIC
  FILES_CMAKE zones_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)
