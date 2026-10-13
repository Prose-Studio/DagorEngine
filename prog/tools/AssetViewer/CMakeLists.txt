# AssetViewer (assetViewer2), the asset viewer and editor: a game on daNetGame (asset_viewer_dng, with the daNetGameLibs
# of av_danetgamelibs.txt) with its own main, on daKernel (the editor tree), with the profiling counters of anim, math
# and fastPhys (DAGOR_MEASURE_PERF) and the ImGui test engine; its asset type plugins are the dirs below
set(deps
  engine.startup engine.math engine.coreUtil engine.workCycle engine.lib3d engine.shaders engine.scene engine.image
  engine.guiBase engine.drv.hid_mouse engine.drv.hid_keyboard engine.drv.drv3d_pc_multi engine.gameRes engine.libFx
  engine.perfMon engine.consoleProc engine.imgui engine.anim engine.animChar engine.phys.fastPhys
  tools.libTools.assetMgr tools.libTools.assetMgrHlp tools.libTools.assetsGui tools.libTools.util
  tools.libTools.renderUtil tools.libTools.shaderResBuilder tools.libTools.EditorCore
  tools.libTools.EditorCore.IEditorCore tools.libTools.fastPhysData tools.libTools.ObjectEditor
  tools.libTools.renderViewports tools.libTools.staticGeom tools.libTools.sceneBuilder tools.libTools.scriptHelpers
  tools.libTools.dtx tools.libTools.ObjCreator3d tools.libTools.winGuiWrapper tools.libTools.staticGeomUi
  tools.libTools.scriptPanelWrapper tools.libTools.math tools.libTools.grsCurView
  tools.sceneTools.daEditorX.services.dngBasedRenderSrv tools.sceneTools.daEditorX.services.dynRenderSrv
  tools.sceneTools.daEditorX.services.wind tools.sceneTools.daEditorX.services.riMgr
  tools.sceneTools.daEditorX.services.prefabMgr tools.sceneTools.daEditorX.services.fxMgr
  tools.sceneTools.daEditorX.services.efxMgr tools.sceneTools.daEditorX.services.physobjMgr
  tools.sceneTools.daEditorX.services.gameobjMgr tools.sceneTools.daEditorX.services.compositMgr
  tools.sceneTools.daEditorX.services.invalidEntityMgr tools.sceneTools.daEditorX.services.bitMaskMgr
  tools.sceneTools.daEditorX.services.dynModelMgr tools.sceneTools.daEditorX.services.animCharMgr
  tools.sceneTools.daEditorX.services.assetSrv tools.sceneTools.daEditorX.services.lightSrv
  tools.sceneTools.daEditorX.services.pixelPerfectSelection tools.sceneTools.daEditorX.services.skiesSrv
  tools.sceneTools.daEditorX.services.colorRangeSrv tools.sceneTools.daEditorX.services.csgEntMgr
  tools.sceneTools.daEditorX.services.cableSrv tools.sceneTools.daEditorX.services.splineGenSrv
  tools.sceneTools.daEditorX.services.ecsMgr tools.sceneTools.daEditorX.services.webui
  tools.sceneTools.daEditorX.services.ecsInput tools.sceneTools.daEditorX.services.visibilityFinderSrv
  tools.sceneTools.impostorBaker.impostorUtil tools.sceneTools.pointCloudGen.generator tools.libTools.propPanel
  tools.libTools.dagFileRW engine.phys.physCommon engine.phys.physBullet engine.phys.physJolt gameLibs.vehiclePhys.jolt
  gameLibs.vehiclePhys.bullet gameLibs.consoleWindow gameLibs.resourcePool gameLibs.render gameLibs.landMesh
  gameLibs.textureUtil gameLibs.render.dof gameLibs.render.wind gameLibs.ecs.rendInst.stub engine.daECS.delayedAct
  gameLibs.quirrel.bindQuirrelEx commonFx.commonFxGame commonFx.commonFxTools tools.AssetViewer.Textures
  tools.AssetViewer.Nodes tools.AssetViewer.Prefabs tools.AssetViewer.LandClass tools.AssetViewer.Materials
  tools.AssetViewer.Splines tools.AssetViewer.collision tools.AssetViewer.Entity tools.AssetViewer.Grass
  tools.AssetViewer.TifMask tools.AssetViewer.physObj tools.AssetViewer.fxEdit tools.AssetViewer.FastPhys
  tools.AssetViewer.Custom tools.AssetViewer.RandomGrass tools.AssetViewer.csgEntity tools.AssetViewer.A2d
  tools.AssetViewer.animTree tools.AssetViewer.dasModules tools.AssetViewer.ecsTemplate 3rdPartyLibs.image.libpng-1.4.22
  3rdPartyLibs.arc.zlib-ng 3rdPartyLibs.image.psdRead 3rdPartyLibs.hash 3rdPartyLibs.ImGuiColorTextEdit
  1stPartyLibs.daScript.modules.dasStdDlg
)
if(WIN32)
  list(APPEND deps engine.drv.hid_dinput engine.drv.hid_gamepad_xinput engine.drv.hid_joystick)
elseif(LINUX)
  list(APPEND deps engine.drv.hid_joystick_linux)
endif()
dagor_add_dng_game(NAME assetViewer2 GAME asset_viewer_dng MAIN_VROM *
  DNG_LIBS av_danetgamelibs.txt
  GAME_LIBS av_gamelibs.txt
  PULLS actInThread_pull
  # the viewer's main is its own: what daNetGame's main and version define, for the game code
  MAIN_CODE "void set_window_title(const char *) {}
void set_fps_limit(int) {}
int get_fps_limit() { return 0; }
void set_corrected_fps_limit(int) {}
void exit_game(const char *, int) {}
void run_main_loop_frame() {}
void (*get_memcollect_cur_thread_cb())() { return nullptr; }
void update_float_exceptions() {}"
  VERSION_CODE "unsigned get_exe_version32() { return 0; }
char const *get_exe_version_str() { return \"0.0.0.0\"; }
int get_build_number() { return -1; }"
  OUTPUT_NAME assetViewer2
  FILES_CMAKE AssetViewer_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/tools/sceneTools/impostorBaker ${DAGOR_PROG_DIR}/tools/sceneTools/pointCloudGen/generator
    ${DAGOR_PROG_DIR}/gameLibs/rendInst
  LINK_OPTIONS PRIVATE "$<$<CXX_COMPILER_FRONTEND_VARIANT:MSVC>:/OPT:NOREF>" # keep what the plugins call
  BUILD_DEPENDENCIES PRIVATE ${deps} tools.libTools.daKernel
  PROPERTIES DAGOR_MEASURE_PERF ON DAGOR_IMGUI_TEST_ENGINE ON
  CDK
)
