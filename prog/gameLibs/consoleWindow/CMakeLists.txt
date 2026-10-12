add_subdirectory(consoleWindowStub)

dagor_add_target(NAME gameLibs.consoleWindow STATIC
  FILES_CMAKE consoleWindow_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
