dagor_add_target(NAME gameLibs.ecs.debug STATIC
  FILES_CMAKE debug_files.cmake
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
)
