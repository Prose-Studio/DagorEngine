dagor_add_target(NAME gameLibs.ecs.lights STATIC
  FILES_CMAKE lights_files.cmake
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
)
