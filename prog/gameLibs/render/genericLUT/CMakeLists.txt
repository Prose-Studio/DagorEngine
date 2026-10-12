dagor_add_target(NAME gameLibs.render.genericLUT STATIC
  FILES_CMAKE genericLUT_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
