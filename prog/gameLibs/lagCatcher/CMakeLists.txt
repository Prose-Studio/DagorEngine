dagor_add_target(NAME gameLibs.lagCatcher STATIC
  FILES_CMAKE lagCatcher_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
