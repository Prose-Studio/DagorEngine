dagor_add_target(NAME gameLibs.publicConfigs STATIC LAX
  FILES_CMAKE publicConfigs_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
