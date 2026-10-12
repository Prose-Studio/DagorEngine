dagor_add_target(NAME gameLibs.render.rtao STATIC
  FILES_CMAKE rtao_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
