dagor_add_target(NAME gameLibs.daSkies2.debug STATIC
  FILES_CMAKE debug_files.cmake
  BUILD_DEPENDENCIES PRIVATE gameLibs.render.daFrameGraph
)
