dagor_add_target(NAME gameLibs.rendInst.riFx STATIC LAX
  FILES_CMAKE riFx_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
