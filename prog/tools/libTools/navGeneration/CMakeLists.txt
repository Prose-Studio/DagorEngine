dagor_add_target(NAME tools.libTools.navGeneration STATIC LAX
  FILES_CMAKE navGeneration_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
