dagor_add_target(NAME gameLibs.ecs.render.weather_effects STATIC
  FILES_CMAKE weather_effects_files.cmake
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
)
