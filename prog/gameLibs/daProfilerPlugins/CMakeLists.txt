dagor_add_target(NAME gameLibs.daProfilerPlugins STATIC
  FILES_CMAKE daProfilerPlugins_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE engine.perfMon
)
