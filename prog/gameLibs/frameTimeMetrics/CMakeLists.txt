dagor_add_target(NAME gameLibs.frameTimeMetrics STATIC LAX
  FILES_CMAKE frameTimeMetrics_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
