dagor_add_target(NAME tools.AssetViewer.Materials STATIC LAX
  FILES_CMAKE Materials_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
)
