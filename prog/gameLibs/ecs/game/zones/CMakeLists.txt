dagor_add_target(NAME gameLibs.ecs.game.zones STATIC
  FILES_CMAKE zones_files.cmake
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)
