dagor_add_target(NAME tools.AssetViewer.Entity STATIC LAX
  FILES_CMAKE Entity_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include ${DAGOR_PROG_DIR}/tools/sceneTools/impostorBaker
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    ${DAGOR_PROG_DIR}/engine/sharedInclude
)
