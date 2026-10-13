# TODO(jam): KernelLinkage ?= dynamic ;
# TODO(jam): include $(Root)/prog/tools/sceneTools/daEditorX/plugin_setup.jam ;

dagor_add_target(NAME staticGeom SHARED LAX
  FILES_CMAKE StaticGeom_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
  BUILD_DEPENDENCIES PRIVATE tools.libTools.winGuiWrapper
)
