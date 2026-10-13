dagor_add_target(NAME tools.sceneTools.daEditorX.services.csgEntMgr STATIC LAX
  FILES_CMAKE csgEntMgr_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/math/carve/include ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.math.carve 3rdPartyLibs.math.poly2tri
  COMPILE_DEFINITIONS PRIVATE NDEBUG CARVE_NODEBUG CARVE_USE_EXACT_PREDICATES
)
