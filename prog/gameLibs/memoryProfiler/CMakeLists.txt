dagor_add_target(NAME gameLibs.memoryProfiler STATIC LAX
  FILES_CMAKE memoryProfiler_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
