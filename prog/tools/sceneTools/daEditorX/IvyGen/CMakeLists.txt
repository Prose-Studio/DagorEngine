# The daEditor3x plugin of ivy generation
include(../daeditorPlugin.cmake)
daeditor_plugin(NAME ivyGen
  FILES_CMAKE IvyGen_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE tools.libTools.winGuiWrapper
)
