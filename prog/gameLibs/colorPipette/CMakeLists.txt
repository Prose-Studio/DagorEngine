dagor_add_target(NAME gameLibs.colorPipette STATIC
  FILES_CMAKE colorPipette_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE gameLibs.gameMath
)
