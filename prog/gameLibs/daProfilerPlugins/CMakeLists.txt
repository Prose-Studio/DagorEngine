dagor_add_target(NAME gameLibs.daProfilerPlugins STATIC
  FILES_CMAKE daProfilerPlugins_files.cmake
  BUILD_DEPENDENCIES PRIVATE engine.perfMon
)
