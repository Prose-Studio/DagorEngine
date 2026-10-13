# TODO(jam): KernelLinkage ?= dynamic ;
# TODO(jam): include $(Root)/prog/tools/sceneTools/daEditorX/plugin_setup.jam ;
# TODO(jam): include $(Root)/prog/3rdPartyLibs/math/carve/carve-options.jam ;

dagor_add_target(NAME csg SHARED LAX
  FILES_CMAKE csg_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE tools.libTools.winGuiWrapper tools.libTools.staticGeom 3rdPartyLibs.math.carve
)
