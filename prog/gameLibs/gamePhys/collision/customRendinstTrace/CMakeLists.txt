dagor_add_target(NAME gameLibs.gamePhys.collision.customRendinstTrace STATIC LAX
  FILES_CMAKE customRendinstTrace_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE gameLibs.landMesh
)
