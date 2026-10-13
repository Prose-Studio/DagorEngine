dagor_add_target(NAME tools.AssetViewer.csgEntity STATIC LAX
  FILES_CMAKE csgEntity_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
