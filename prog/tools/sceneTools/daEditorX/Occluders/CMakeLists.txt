# The daEditor3x plugin of occluders
include(../daeditorPlugin.cmake)
daeditor_plugin(NAME occluders
  FILES_CMAKE Occluders_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE tools.libTools.winGuiWrapper
)
