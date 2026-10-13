dagor_add_target(NAME gameLibs.ecs.weather STATIC
  FILES_CMAKE weather_files.cmake
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
)
