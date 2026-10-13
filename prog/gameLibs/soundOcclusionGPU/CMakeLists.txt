dagor_add_target(NAME gameLibs.soundOcclusionGPU STATIC
  FILES_CMAKE soundOcclusionGPU_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
  BUILD_DEPENDENCIES PRIVATE engine.lib3d gameLibs.daSDF
)
