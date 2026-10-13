dagor_add_target(NAME gameLibs.render.outline STATIC
  FILES_CMAKE outline_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
)
