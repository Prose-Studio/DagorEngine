dagor_add_target(NAME tools.AssetViewer.RandomGrass STATIC LAX
  FILES_CMAKE RandomGrass_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
