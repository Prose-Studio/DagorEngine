dagor_add_target(NAME gameLibs.render.psoCacheLoader STATIC
  FILES_CMAKE psoCacheLoader_files.cmake
  BUILD_DEPENDENCIES PRIVATE engine.lib3d
)
