# TODO(jam): KernelLinkage ?= dynamic ;
# TODO(jam): UseD3DMulti = yes ;
dagor_add_target(NAME tools.sceneTools.impostorBaker.impostorUtil STATIC LAX
  FILES_CMAKE impostorUtil_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/gameLibs/render
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.image.tiff-4.4.0
)
