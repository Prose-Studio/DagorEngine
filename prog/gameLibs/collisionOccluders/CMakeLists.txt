dagor_add_target(NAME gameLibs.collisionOccluders STATIC
  FILES_CMAKE collisionOccluders_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
