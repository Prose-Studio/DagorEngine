dagor_add_target(NAME tools.AssetViewer.Custom STATIC LAX
  FILES_CMAKE Custom_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
)
