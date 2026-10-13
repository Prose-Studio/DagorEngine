# Ambient occlusion (SSAO, GTAO, mobile SSAO; a gameLibs module): its users add this dir to their include dirs
dagor_add_dng_module(NAME gameLibs.render.ambientOcclusion
  FILES_CMAKE ambientOcclusion_files.cmake
  BUILD_DEPENDENCIES PRIVATE gameLibs.render
)
