dagor_add_target(NAME tools.AssetViewer.Grass STATIC LAX
  FILES_CMAKE Grass_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
)
