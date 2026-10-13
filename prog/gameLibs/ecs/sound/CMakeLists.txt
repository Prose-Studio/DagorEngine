dagor_add_target(NAME gameLibs.ecs.sound STATIC
  FILES_CMAKE sound_files.cmake
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
)
