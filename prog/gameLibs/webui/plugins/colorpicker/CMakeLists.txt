dagor_add_target(NAME gameLibs.webui.plugins.colorpicker STATIC
  FILES_CMAKE colorpicker_files.cmake
  BUILD_DEPENDENCIES PRIVATE gameLibs.colorPipette
)
