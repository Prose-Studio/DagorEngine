dagor_add_target(NAME gameLibs.consoleKeyBindings STATIC
  FILES_CMAKE consoleKeyBindings_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
