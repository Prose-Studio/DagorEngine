dagor_add_target(NAME tools.AssetViewer.ecsTemplate STATIC LAX
  FILES_CMAKE ecsTemplate_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE tools.libTools.ecsPropPanel
)
