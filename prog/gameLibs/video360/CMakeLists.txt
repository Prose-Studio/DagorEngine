dagor_add_target(NAME gameLibs.video360 STATIC
  FILES_CMAKE video360_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
