dagor_add_target(NAME tools.AssetViewer.fxEdit STATIC LAX
  FILES_CMAKE fxEdit_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/gameLibs/squirrel ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
)
