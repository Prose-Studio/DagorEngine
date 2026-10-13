dagor_add_target(NAME gameLibs.ecs.input STATIC
  FILES_CMAKE input_files.cmake
  BUILD_DEPENDENCIES PRIVATE gameLibs.daInput
)
