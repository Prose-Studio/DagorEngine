# daEditor3x, the level editor: a game on daNetGame (editor_dng, with the daNetGameLibs of editor_danetgamelibs.txt)
# with its own main, on daKernel (the editor tree), its plugins in plugins/daEditorX (daeditor_plugin, the plugin dirs)
set(deps
  engine.startup engine.math engine.lib3d engine.shaders engine.guiBase engine.osApiWrappers.messageBox engine.workCycle
  engine.drv.drv3d_pc_multi engine.drv.hid_mouse engine.drv.hid_keyboard engine.anim engine.animChar engine.gameRes
  engine.phys.fastPhys engine.libFx engine.image engine.coreUtil engine.scene engine.streaming tools.libTools.propPanel
  tools.libTools.util tools.libTools.renderViewports tools.libTools.renderUtil tools.libTools.shaderResBuilder
  tools.libTools.EditorCore tools.libTools.EditorCore.IEditorCore tools.libTools.ObjCreator3d tools.libTools.grsCurView
  engine.phys.physCommon engine.phys.physBullet engine.perfMon engine.collResDebugDraw engine.consoleProc
  tools.libTools.dagFileRW tools.libTools.dtx tools.libTools.texConverter tools.libTools.staticGeom
  tools.libTools.staticGeomImp tools.libTools.sceneBuilder tools.libTools.unwrapMapping tools.libTools.coolConsole
  tools.libTools.delaunay tools.libTools.assetMgr tools.libTools.assetsGui tools.libTools.assetMgrHlp
  tools.libTools.winGuiWrapper tools.sceneTools.daEditorX.ecsEditor tools.sceneTools.daEditorX.Environment
  tools.sceneTools.daEditorX.Collision tools.sceneTools.daEditorX.ScnExport tools.sceneTools.daEditorX.ssView
  tools.sceneTools.daEditorX.binSceneView tools.sceneTools.daEditorX.services.dngBasedRenderSrv
  tools.sceneTools.daEditorX.services.dynRenderSrv tools.sceneTools.daEditorX.services.riMgr
  tools.sceneTools.daEditorX.services.pixelPerfectSelection tools.sceneTools.daEditorX.services.prefabMgr
  tools.sceneTools.daEditorX.services.fxMgr tools.sceneTools.daEditorX.services.efxMgr
  tools.sceneTools.daEditorX.services.physobjMgr tools.sceneTools.daEditorX.services.gameobjMgr
  tools.sceneTools.daEditorX.services.compositMgr tools.sceneTools.daEditorX.services.entFilters
  tools.sceneTools.daEditorX.services.bitMaskMgr tools.sceneTools.daEditorX.services.hmapDebugShadingSrv
  tools.sceneTools.daEditorX.services.hmapSrv tools.sceneTools.daEditorX.services.assetSrv
  tools.sceneTools.daEditorX.services.builtSceneView tools.sceneTools.daEditorX.services.lightSrv
  tools.sceneTools.daEditorX.services.fileTracker tools.sceneTools.daEditorX.services.invalidEntityMgr
  tools.sceneTools.daEditorX.services.carCamera tools.sceneTools.daEditorX.services.animCharMgr
  tools.sceneTools.daEditorX.services.dynModelMgr tools.sceneTools.daEditorX.services.skiesSrv
  tools.sceneTools.daEditorX.services.colorRangeSrv tools.sceneTools.daEditorX.services.grassSrv
  tools.sceneTools.daEditorX.services.waterSrv tools.sceneTools.daEditorX.services.csgEntMgr
  tools.sceneTools.daEditorX.services.waterProjFxSrv tools.sceneTools.daEditorX.services.cableSrv
  tools.sceneTools.daEditorX.services.splineGenSrv tools.sceneTools.daEditorX.services.ecsMgr
  tools.sceneTools.daEditorX.services.visibilityFinderSrv tools.sceneTools.daEditorX.services.webui
  tools.sceneTools.daEditorX.services.wind 3rdPartyLibs.image.psdRead 3rdPartyLibs.image.libpng-1.4.22
  3rdPartyLibs.arc.zlib-ng 3rdPartyLibs.hash commonFx.commonFxGame gameLibs.consoleWindow gameLibs.resourcePool
  gameLibs.heightmap gameLibs.render gameLibs.rendInst gameLibs.render.cables gameLibs.render.dof gameLibs.render.wind
  gameLibs.render.nodeBasedShader gameLibs.render.fx engine.daECS.hierarchyTransform gameLibs.ecs.rendInst.stub
  engine.daECS.gameResStub engine.daECS.scene engine.daECS.delayedAct gameLibs.daFx gameLibs.eventLog
  gameLibs.vehiclePhys.bullet gameLibs.landMesh gameLibs.textureUtil gameLibs.textureGen 3rdPartyLibs.image.tiff-4.4.0
  gameLibs.imguiInput gameLibs.physMap 1stPartyLibs.daScript.modules.dasStdDlg
)
if(WIN32)
  list(APPEND deps engine.drv.hid_dinput engine.drv.hid_gamepad_xinput engine.drv.hid_joystick System::advapi32
    System::htmlhelp System::psapi)
elseif(LINUX)
  list(APPEND deps engine.drv.hid_joystick_linux)
endif()
dagor_add_dng_game(NAME daEditor3x GAME editor_dng MAIN_VROM *
  DNG_LIBS editor_danetgamelibs.txt
  GAME_LIBS editor_gamelibs.txt
  PULLS actInThread_pull
  # the editor's main is its own (dagored_main.cpp): what daNetGame's main and version define, for the game code
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
  OUTPUT_NAME daEditor3x
  FILES_CMAKE daEditorX_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    include ${DAGOR_PROG_DIR}/tools/sharedInclude ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  LINK_OPTIONS PRIVATE "$<$<CXX_COMPILER_FRONTEND_VARIANT:MSVC>:/OPT:NOREF>" # keep what the plugins call
  BUILD_DEPENDENCIES PRIVATE ${deps} tools.libTools.daKernel
  PROPERTIES DAGOR_FRAME_LIMIT 262144 DAGOR_IMGUI_TEST_ENGINE ON
  CDK
)
