dagor_add_target(NAME gameLibs.render.ptgi STATIC
  FILES_CMAKE ptgi_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
