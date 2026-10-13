dagor_add_target(NAME tools.AssetViewer.Splines STATIC LAX
  FILES_CMAKE Splines_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
