dagor_add_target(NAME gameLibs.grid STATIC
  FILES_CMAKE grid_files.cmake
  BUILD_DEPENDENCIES PRIVATE gameLibs.gameMath
)
