dagor_add_target(NAME gameLibs.render.upscale STATIC
  FILES_CMAKE upscale_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/render
)
