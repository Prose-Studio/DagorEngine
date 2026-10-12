dagor_add_target(NAME gameLibs.fpsProfiler STATIC
  FILES_CMAKE fpsProfiler_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
