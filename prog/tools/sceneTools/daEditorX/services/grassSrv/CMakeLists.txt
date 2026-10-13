dagor_add_target(NAME tools.sceneTools.daEditorX.services.grassSrv STATIC LAX
  FILES_CMAKE grassSrv_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
