dagor_add_target(NAME gameLibs.grid STATIC
  FILES_CMAKE grid_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE gameLibs.gameMath
)
