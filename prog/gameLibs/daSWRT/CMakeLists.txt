dagor_add_target(NAME gameLibs.daSWRT STATIC
  FILES_CMAKE daSWRT_files.cmake
  BUILD_DEPENDENCIES PRIVATE engine.lib3d engine.daBVH
)
