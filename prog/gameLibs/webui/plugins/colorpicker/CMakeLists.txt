dagor_add_target(NAME gameLibs.webui.plugins.colorpicker STATIC
  FILES_CMAKE colorpicker_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE gameLibs.colorPipette
)
