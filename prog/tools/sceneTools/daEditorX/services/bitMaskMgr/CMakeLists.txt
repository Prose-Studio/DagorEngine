# daEditorX bitmask image manager service (IBitMaskImageMgr) on libtiff
set(includes ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include ${DAGOR_PROG_DIR}/tools/sharedInclude)
set(sources bitMaskMgr.cpp)
set(deps 3rdPartyLibs.image.tiff-4.4.0)

dagor_add_library(tools.sceneTools.daEditorX.services.bitMaskMgr LAX ${sources})
target_include_directories(tools.sceneTools.daEditorX.services.bitMaskMgr PRIVATE ${includes})
target_link_libraries(tools.sceneTools.daEditorX.services.bitMaskMgr PRIVATE ${deps})
