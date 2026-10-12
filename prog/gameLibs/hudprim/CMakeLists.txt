dagor_add_target(NAME gameLibs.hudprim STATIC LAX
  FILES_CMAKE hudprim_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
