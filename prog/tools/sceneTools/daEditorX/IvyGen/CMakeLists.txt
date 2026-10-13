# TODO(jam): KernelLinkage ?= dynamic ;
# TODO(jam): include $(Root)/prog/tools/sceneTools/daEditorX/plugin_setup.jam ;

dagor_add_target(NAME ivyGen SHARED LAX
  FILES_CMAKE IvyGen_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE tools.libTools.winGuiWrapper
)
