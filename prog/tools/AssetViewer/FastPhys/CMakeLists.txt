dagor_add_target(NAME tools.AssetViewer.FastPhys STATIC LAX
  FILES_CMAKE FastPhys_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
