dagor_add_target(NAME tools.sceneTools.daEditorX.services.gameobjMgr STATIC LAX
  FILES_CMAKE gameobjMgr_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
)
