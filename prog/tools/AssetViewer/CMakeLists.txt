# TODO(jam): KernelLinkage ?= dynamic ;
# TODO(jam): BuildingTools = yes ;
# TODO(jam): PhysName = Jolt ;
# TODO(jam): UseD3DMulti = yes ;
# TODO(jam): UseD3DMultiForced ?= windows linux ;
# TODO(jam): if ! $(UseD3DMultiList) { UseD3DMultiList_windows = DX11 vulkan ; UseD3DMultiList_linux = vulkan ; }
# TODO(jam): if $(CheckOnly) = yes { DisableUsingPCH = yes ; }
# TODO(jam): CheckedContainers = no ;
# TODO(jam): UseMemoryDebugLevel = def ;
# TODO(jam): HaveOverlayUI = no ;
# TODO(jam): HaveDngInput = no ;
# TODO(jam): HaveEditor = no ;
# TODO(jam): HaveConsole = no ;
# TODO(jam): HaveSound = no ;
# TODO(jam): HaveSoundNet = no ;
# TODO(jam): ImguiTestRuntime ?= yes ;
# TODO(jam): VRDeviceSupport = yes ;
# TODO(jam): VRDeviceOptional = yes ;
# TODO(jam): ToolsHaveVR ?= yes ;
# TODO(jam): DagorAnim_MEASURE_PERF = 1 ;
# TODO(jam): DagorMath_MEASURE_PERF = 1 ;
# TODO(jam): DagorFastPhys_MEASURE_PERF = 1 ;
# TODO(jam): DagorAnim_MEASURE_PERF_FRAMES = 1000 ;
# TODO(jam): DagorMath_MEASURE_PERF_FRAMES = 1000 ;
# TODO(jam): DagorFastPhys_MEASURE_PERF_FRAMES = 1000 ;
# TODO(jam): DafxGravityZone ?= yes ;
set(deps
  engine.startup
  engine.math
  engine.coreUtil
  engine.workCycle
  engine.lib3d
  engine.shaders
  engine.scene
  engine.image
  engine.guiBase
  engine.drv.hid_mouse
  engine.drv.hid_keyboard
  engine.drv.drv3d_pc_multi
  engine.gameRes
  engine.libFx
  engine.perfMon
  engine.consoleProc
  engine.imgui
  engine.anim
  engine.animChar
  engine.phys.fastPhys
  tools.libTools.assetMgr
  tools.libTools.assetMgrHlp
  tools.libTools.assetsGui
  tools.libTools.util
  tools.libTools.renderUtil
  tools.libTools.shaderResBuilder
  tools.libTools.EditorCore
  tools.libTools.EditorCore.IEditorCore
  tools.libTools.fastPhysData
  tools.libTools.ObjectEditor
  tools.libTools.renderViewports
  tools.libTools.staticGeom
  tools.libTools.sceneBuilder
  tools.libTools.scriptHelpers
  tools.libTools.dtx
  tools.libTools.ObjCreator3d
  tools.libTools.winGuiWrapper
  tools.libTools.staticGeomUi
  tools.libTools.scriptPanelWrapper
  tools.libTools.math
  tools.libTools.grsCurView
  tools.sceneTools.daEditorX.services.dngBasedRenderSrv
  tools.sceneTools.daEditorX.services.dynRenderSrv
  tools.sceneTools.daEditorX.services.wind
  tools.sceneTools.daEditorX.services.riMgr
  tools.sceneTools.daEditorX.services.prefabMgr
  tools.sceneTools.daEditorX.services.fxMgr
  tools.sceneTools.daEditorX.services.efxMgr
  tools.sceneTools.daEditorX.services.physobjMgr
  tools.sceneTools.daEditorX.services.gameobjMgr
  tools.sceneTools.daEditorX.services.compositMgr
  tools.sceneTools.daEditorX.services.invalidEntityMgr
  tools.sceneTools.daEditorX.services.bitMaskMgr
  tools.sceneTools.daEditorX.services.dynModelMgr
  tools.sceneTools.daEditorX.services.animCharMgr
  tools.sceneTools.daEditorX.services.assetSrv
  tools.sceneTools.daEditorX.services.lightSrv
  tools.sceneTools.daEditorX.services.dynModelMgr
  tools.sceneTools.daEditorX.services.physobjMgr
  tools.sceneTools.daEditorX.services.pixelPerfectSelection
  tools.sceneTools.daEditorX.services.skiesSrv
  tools.sceneTools.daEditorX.services.colorRangeSrv
  tools.sceneTools.daEditorX.services.csgEntMgr
  tools.sceneTools.daEditorX.services.cableSrv
  tools.sceneTools.daEditorX.services.splineGenSrv
  tools.sceneTools.daEditorX.services.ecsMgr
  tools.sceneTools.daEditorX.services.webui
  tools.sceneTools.daEditorX.services.ecsInput
  tools.sceneTools.daEditorX.services.visibilityFinderSrv
  tools.sceneTools.impostorBaker.impostorUtil
  tools.sceneTools.pointCloudGen.generator
  tools.libTools.propPanel
  tools.libTools.dagFileRW
  engine.phys.physCommon
  engine.phys.physBullet
  engine.phys.physJolt
  gameLibs.vehiclePhys.vehiclePhys-JOLT
  gameLibs.vehiclePhys.vehiclePhys-BULLET
  gameLibs.consoleWindow
  gameLibs.resourcePool
  gameLibs.render
  gameLibs.landMesh
  gameLibs.textureUtil
  gameLibs.render.dof
  gameLibs.render.wind
  gameLibs.ecs.rendInst.stub
  engine.daECS.delayedAct
  gameLibs.quirrel.bindQuirrelEx
  commonFx.commonFxGame
  commonFx.commonFxTools
  tools.AssetViewer.Textures
  tools.AssetViewer.Nodes
  tools.AssetViewer.Prefabs
  tools.AssetViewer.LandClass
  tools.AssetViewer.Materials
  tools.AssetViewer.Splines
  tools.AssetViewer.collision
  tools.AssetViewer.Entity
  tools.AssetViewer.Grass
  tools.AssetViewer.TifMask
  tools.AssetViewer.physObj
  tools.AssetViewer.fxEdit
  tools.AssetViewer.FastPhys
  tools.AssetViewer.Custom
  tools.AssetViewer.RandomGrass
  tools.AssetViewer.csgEntity
  tools.AssetViewer.A2d
  tools.AssetViewer.animTree
  tools.AssetViewer.dasModules
  tools.AssetViewer.ecsTemplate
  3rdPartyLibs.image.libpng-1.4.22
  3rdPartyLibs.arc.zlib-ng
  3rdPartyLibs.image.psdRead
  3rdPartyLibs.hash
  3rdPartyLibs.ImGuiColorTextEdit
  daNetGame
  1stPartyLibs.daScript.modules.dasStdDlg
)
if(WIN32)
  list(APPEND deps engine.drv.hid_dinput engine.drv.hid_gamepad_xinput engine.drv.hid_joystick)
elseif(LINUX)
  list(APPEND deps engine.drv.hid_joystick_linux)
else()
  # TODO(jam): Exit unsupported Platform\=$(Platform) for Target\=$(Target) ;
endif()
# TODO(jam): gamePulls = daECS/core/componentType.h game_pulls ;
# TODO(jam): if $(VRDeviceSupport) = yes { include $(Root)/prog/engine/drv/vr_device/bundle.jam ; }
if(IS_DIRECTORY "${DAGOR_ENGINE_ROOT}/skyquake/prog/tools")
  # TODO(jam): UseRootLibs = skyquake/prog/tools/wtUnit_av2 ;
  list(APPEND defines HAS_PLUGIN_WT_UNIT)
endif()
dagor_game_lib(PULLS actInThread_pull)
# TODO(jam): ImportProgLibs = tools/libTools/daKernel ;
# TODO(jam): if $(Platform) = windows && ! $(DagoredRel) { LINKopt = -opt:noref ; } else if $(Platform) = linux {
#   LINKopt += -L$(Root)/tools/dagor_cdk/$(Platform)-$(PlatformArch) ; }
# TODO(jam): Game = asset_viewer_dng ;
# TODO(jam): GameMainVromFilePath = * ;
set(GameMainVromMountDir *)
# TODO(jam): include $(Root)/prog/daNetGame/game.jam ;
# TODO(jam): gameMain = void set_window_title(const char *){} void set_fps_limit(int){} int
#   get_fps_limit(){return 0;} void set_corrected_fps_limit(int){} void exit_game(const char *, int){}
#   void run_main_loop_frame(){} ;
if(DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  # TODO(jam): gameMain += void (*get_memcollect_cur_thread_cb())(){ return nullptr;} void
  #   update_float_exceptions(){} ;
  set(ImportsRelativeDir .)
endif()

dagor_add_target(NAME assetViewer2 EXECUTABLE WIN32 LAX
  FILES_CMAKE AssetViewer_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/tools/sceneTools/impostorBaker
    ${DAGOR_PROG_DIR}/tools/sceneTools/pointCloudGen/generator ${DAGOR_PROG_DIR}/gameLibs/rendInst
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PRIVATE ${deps} Dagor::Quirrel
  PROPERTIES DAGOR_EXCEPTIONS ON
  CDK
)
