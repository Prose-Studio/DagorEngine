dagor_add_target(NAME gameLibs.visualConsole STATIC
  FILES_CMAKE visualConsole_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
