dagor_add_target(NAME gameLibs.iblCube STATIC LAX
  FILES_CMAKE iblCube_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
