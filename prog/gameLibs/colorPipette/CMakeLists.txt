dagor_add_target(NAME gameLibs.colorPipette STATIC
  FILES_CMAKE colorPipette_files.cmake
  BUILD_DEPENDENCIES PRIVATE gameLibs.gameMath
)
