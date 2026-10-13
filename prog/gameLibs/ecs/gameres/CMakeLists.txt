dagor_add_target(NAME gameLibs.ecs.gameres STATIC
  FILES_CMAKE gameres_files.cmake
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
)
