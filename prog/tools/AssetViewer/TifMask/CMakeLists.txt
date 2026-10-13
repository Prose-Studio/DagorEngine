dagor_add_target(NAME tools.AssetViewer.TifMask STATIC LAX
  FILES_CMAKE TifMask_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
)
