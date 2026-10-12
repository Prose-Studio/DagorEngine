# Graph layout for node graph visualizations
dagor_add_target(NAME gameLibs.graphLayouter STATIC
  FILES_CMAKE graphLayouter_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
