dagor_add_dng_module(NAME gameLibs.voxelizedMedia
  FILES_CMAKE voxelizedMedia_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR} shaders
  BUILD_DEPENDENCIES PRIVATE engine.lib3d
)
