# TODO(jam): KernelLinkage ?= dynamic ;
# TODO(jam): include $(Root)/prog/tools/sceneTools/daEditorX/plugin_setup.jam ;

dagor_add_target(NAME graphEditor SHARED LAX
  FILES_CMAKE GraphEditor_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui-node-editor
  BUILD_DEPENDENCIES PRIVATE
    3rdPartyLibs.imgui-node-editor engine.coreUtil tools.libTools.graphEditor tools.libTools.winGuiWrapper
)
