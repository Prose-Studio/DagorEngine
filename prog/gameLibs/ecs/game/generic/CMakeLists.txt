dagor_add_target(NAME gameLibs.ecs.game.generic STATIC
  FILES_CMAKE generic_files.cmake
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel 3rdPartyLibs.eastl Dagor::Phys
)
