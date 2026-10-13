dagor_add_target(NAME tools.AssetViewer.animTree STATIC LAX
  FILES_CMAKE animTree_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/gameLibs
)
