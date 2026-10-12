dagor_add_target(NAME gameLibs.render.rtr STATIC
  FILES_CMAKE rtr_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
