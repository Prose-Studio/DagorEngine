dagor_add_target(NAME gameLibs.nodeBasedShaderManager STATIC
  FILES_CMAKE nodeBasedShaderManager_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
