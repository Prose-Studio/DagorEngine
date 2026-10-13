# The daEditor3x plugin of static geometry
include(../daeditorPlugin.cmake)
daeditor_plugin(NAME staticGeom
  FILES_CMAKE StaticGeom_files.cmake
  BUILD_DEPENDENCIES PRIVATE tools.libTools.winGuiWrapper
)
