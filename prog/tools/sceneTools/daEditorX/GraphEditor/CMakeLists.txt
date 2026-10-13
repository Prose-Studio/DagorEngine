# The daEditor3x plugin of the node graph editor
include(../daeditorPlugin.cmake)
daeditor_plugin(NAME graphEditor
  FILES_CMAKE GraphEditor_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui-node-editor
  BUILD_DEPENDENCIES PRIVATE
    3rdPartyLibs.imgui-node-editor engine.coreUtil tools.libTools.graphEditor tools.libTools.winGuiWrapper
)
