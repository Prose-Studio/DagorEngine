dagor_add_target(NAME gameLibs.propsRegistry STATIC LAX
  FILES_CMAKE propsRegistry_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
