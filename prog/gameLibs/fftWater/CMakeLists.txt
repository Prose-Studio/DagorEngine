dagor_add_target(NAME gameLibs.fftWater STATIC LAX
  FILES_CMAKE fftWater_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/fftWater/fftCPU
  BUILD_DEPENDENCIES PRIVATE gameLibs.heightmap engine.lib3d
)
