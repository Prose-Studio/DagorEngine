add_subdirectory(timers)

dagor_add_target(NAME gameLibs.daGame STATIC LAX
  FILES_CMAKE daGame_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
