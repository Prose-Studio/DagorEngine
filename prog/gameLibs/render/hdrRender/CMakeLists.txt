dagor_add_target(NAME gameLibs.render.hdrRender STATIC
  FILES_CMAKE hdrRender_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
