add_subdirectory(stub)

dagor_add_target(NAME gameLibs.gamePhys.props STATIC
  FILES_CMAKE props_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
