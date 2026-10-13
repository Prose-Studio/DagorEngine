# The daEditor3x plugin of CSG objects (on carve)
include(../daeditorPlugin.cmake)
daeditor_plugin(NAME csg
  FILES_CMAKE csg_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/math/carve/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  COMPILE_DEFINITIONS PRIVATE NDEBUG CARVE_NODEBUG CARVE_USE_EXACT_PREDICATES
  BUILD_DEPENDENCIES PRIVATE tools.libTools.winGuiWrapper tools.libTools.staticGeom 3rdPartyLibs.math.carve
)
