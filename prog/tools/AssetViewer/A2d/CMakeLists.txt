dagor_add_target(NAME tools.AssetViewer.A2d STATIC LAX
  FILES_CMAKE A2d_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    ${DAGOR_PROG_DIR}/3rdPartyLibs/acl/includes
)
