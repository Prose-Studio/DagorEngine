# TODO(jam): KernelLinkage = dynamic ;
# TODO(jam): UseD3DMulti = yes ;
# TODO(jam): UseD3DMultiList = DX11 stub ;
# TODO(jam): ImportProgLibs = tools/libTools/daKernel ;
# TODO(jam): if ! $(DagoredRel) { LINKopt = -opt:noref ; }

dagor_add_target(NAME blkEditor EXECUTABLE WIN32 LAX
  FILES_CMAKE blkEditor_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/scintilla/include ${DAGOR_PROG_DIR}/3rdPartyLibs/lexilla/include
  BUILD_DEPENDENCIES PRIVATE
    engine.startup engine.math engine.workCycle engine.lib3d engine.shaders engine.image engine.imgui
    engine.drv.drv3d_pc_multi engine.drv.hid_mouse engine.drv.hid_keyboard tools.libTools.EditorCore
    tools.libTools.propPanel tools.libTools.winGuiWrapper tools.libTools.scriptPanelWrapper tools.libTools.coolConsole
    tools.libTools.util 3rdPartyLibs.arc.zlib-ng System::comctl32
  CDK
)
