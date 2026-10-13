dagor_add_target(NAME gameLibs.gamePhys.collision.customRendinstTrace STATIC LAX
  FILES_CMAKE customRendinstTrace_files.cmake
  BUILD_DEPENDENCIES PRIVATE gameLibs.landMesh
)
