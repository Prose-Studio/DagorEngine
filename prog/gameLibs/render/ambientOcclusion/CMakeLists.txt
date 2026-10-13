# Ambient occlusion (SSAO, GTAO, mobile SSAO; a gameLibs module): its headers are in this dir
dagor_add_dng_module(NAME gameLibs.render.ambientOcclusion
  FILES_CMAKE ambientOcclusion_files.cmake
  INCLUDE_DIRECTORIES PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}
  BUILD_DEPENDENCIES PRIVATE gameLibs.render
)
