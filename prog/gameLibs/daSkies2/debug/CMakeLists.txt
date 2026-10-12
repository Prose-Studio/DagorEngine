dagor_add_target(NAME gameLibs.daSkies2.debug STATIC
  FILES_CMAKE debug_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE gameLibs.render.daFrameGraph
)
