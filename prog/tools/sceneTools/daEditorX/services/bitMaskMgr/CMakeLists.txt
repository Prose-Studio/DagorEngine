# daEditorX bitmask image manager service (IBitMaskImageMgr) on libtiff
dagor_add_target(NAME tools.sceneTools.daEditorX.services.bitMaskMgr STATIC LAX
  FILES_CMAKE bitMaskMgr_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.image.tiff-4.4.0
)
