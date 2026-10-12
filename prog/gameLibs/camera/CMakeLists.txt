dagor_add_target(NAME gameLibs.camera STATIC
  FILES_CMAKE camera_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
