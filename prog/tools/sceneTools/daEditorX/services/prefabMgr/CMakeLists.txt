dagor_add_target(NAME tools.sceneTools.daEditorX.services.prefabMgr STATIC LAX
  FILES_CMAKE prefabMgr_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
