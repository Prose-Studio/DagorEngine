# daNetGame: the framework of the games on it (the client or the dedicated server of a game tree, DAGOR_DEDICATED),
# which link it with their own code (dagor_add_dng_game). Its switches are the tree's (DagorGame.cmake); those that
# off in Rel are generator expressions here, so these lists have parts that only some configurations build.
set(deps)
set(pulls)
set(system_libs)

# _dng_not(<out> <cond>): the negation of a condition
function(_dng_not out cond)
  if(cond STREQUAL "0")
    set(${out} 1 PARENT_SCOPE)
  elseif(cond STREQUAL "1")
    set(${out} 0 PARENT_SCOPE)
  else()
    set(${out} "$<NOT:${cond}>" PARENT_SCOPE)
  endif()
endfunction()

# _dng_deps(<cond> <target>... [ELSE <target>...]): the libraries linked where <cond> holds, and those linked elsewhere
function(_dng_deps cond)
  cmake_parse_arguments(PARSE_ARGV 1 arg "" "" "ELSE")
  set(result ${deps})
  if(cond STREQUAL "1")
    list(APPEND result ${arg_UNPARSED_ARGUMENTS})
  elseif(cond STREQUAL "0")
    list(APPEND result ${arg_ELSE})
  else()
    foreach(name IN LISTS arg_UNPARSED_ARGUMENTS)
      list(APPEND result "$<${cond}:${name}>")
    endforeach()
    foreach(name IN LISTS arg_ELSE)
      list(APPEND result "$<$<NOT:${cond}>:${name}>")
    endforeach()
  endif()
  set(deps ${result} PARENT_SCOPE)
endfunction()

set(dev "$<NOT:$<CONFIG:Rel>>")
set(desktop OFF)
if(CMAKE_SYSTEM_NAME MATCHES "^(Darwin|Linux|Windows)$")
  set(desktop ON)
endif()
set(desktop_dev 0)
if(desktop)
  set(desktop_dev "${dev}")
endif()
set(renderer 0)
if(DAGOR_GAME_RENDERER)
  set(renderer 1)
endif()
set(imgui "${DAGOR_GAME_IMGUI}")
_dng_not(no_imgui "${imgui}")
set(editor "${DAGOR_GAME_EDITOR}")
_dng_not(no_editor "${editor}")
set(webui "${DAGOR_GAME_WEBUI}")
_dng_not(no_webui "${webui}")

# the memory manager: the debug allocator outside Rel on Windows, the system's on the Linux servers and with sanitizers
set(memory_leaks 0)
if(NOT DAGOR_SANITIZE STREQUAL "none")
  set(memory engine.memory.default.off)
elseif(WIN32)
  set(memory "$<IF:$<CONFIG:Rel>,engine.memory.rtl,engine.memory.default.dbg>")
  set(memory_leaks "${dev}")
elseif(LINUX AND DAGOR_DEDICATED)
  set(memory engine.memory.default.off)
else()
  set(memory engine.memory)
endif()
_dng_not(no_memory_leaks "${memory_leaks}")

# --- the libraries ---------------------------------------------------------------------------------------------------
if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  # the memory manager before the other libraries, for its static initializers to come early
  list(APPEND deps engine.osApiWrappers engine.kernel ${memory} engine.ioSys engine.baseUtil)
endif()
list(APPEND deps engine.startup engine.coreUtil engine.math engine.lib3d engine.image engine.unitTest engine.shaders
  engine.streaming engine.workCycle engine.guiBase engine.scene engine.phys.physCommon engine.animChar engine.anim
  engine.phys.fastPhys engine.ADT engine.crypto engine.gameRes engine.perfMon engine.profilerTracker
  gameLibs.daProfilerPlugins gameLibs.digitalSignature gameLibs.decalMatrices gameLibs.quirrel.sqDebugger
  gameLibs.quirrel.clientLog gameLibs.quirrel.sqJwt gameLibs.quirrel.yupfile_parse gameLibs.yup_parse gameLibs.fftWater
  gameLibs.heightmap engine.daNet gameLibs.daFracture.core gameLibs.daPhys gameLibs.physMap
  gameLibs.gamePhys.collision.collision-common gameLibs.gamePhys.collision.customRendinstTrace
  gameLibs.gamePhys.collision.rendinst gameLibs.gamePhys.props gameLibs.gamePhys.phys gameLibs.gamePhys.common
  gameLibs.sepClientInstance gameLibs.gameMath gameLibs.grid gameLibs.lagCatcher gameLibs.landMesh gameLibs.rendInst
  gameLibs.memoryProfiler gameLibs.camera gameLibs.camTrack gameLibs.folders gameLibs.webvromfs gameLibs.levelSplines
  gameLibs.dataBlockUtils gameLibs.dataBlockUtils.blk2sqrat gameLibs.jsonUtils gameLibs.video360 gameLibs.streaming
  gameLibs.smokeOccluder gameLibs.hudprim gameLibs.perFrameStat engine.consoleProc engine.imgui gameLibs.daGame
  gameLibs.daGame.timers gameLibs.quirrel.bindQuirrelEx gameLibs.quirrel.sqCrossCall gameLibs.quirrel.quirrel_json
  gameLibs.quirrel.sqConsole gameLibs.quirrel.http gameLibs.quirrel.asyncRuntime gameLibs.quirrel.sqDacoll
  gameLibs.quirrel.sqStatsd gameLibs.quirrel.base64 gameLibs.quirrel.sqDataCache gameLibs.quirrel.nestdb
  gameLibs.quirrel.sqSysInfo gameLibs.quirrel.lastInputMonitor gameLibs.quirrel.sqPerFrameStat gameLibs.ecs.scripts.das
  gameLibs.ecs.scripts.dasSq gameLibs.dasModules.common gameLibs.dasModules.appTime gameLibs.dasModules.quirrel
  gameLibs.dasModules.phys gameLibs.dasModules.generic gameLibs.dasModules.ECSGlobalTags
  gameLibs.dasModules.currentCircuit gameLibs.dasModules.gameMath gameLibs.dasModules.rendInst
  gameLibs.dasModules.daInput gameLibs.dasModules.actions gameLibs.dasModules.daProfiler
  gameLibs.dasModules.forceFeedback gameLibs.dasModules.net gameLibs.dasModules.statsd
  gameLibs.dasModules.gpuReadbackQuery gameLibs.dasModules.landMesh gameLibs.dasModules.systemInfo
  gameLibs.dasModules.compressionUtils gameLibs.dasModules.perFrameStat gameLibs.das.ecs gameLibs.das.math
  gameLibs.propsRegistry engine.daECS.core engine.daECS.net engine.daECS.net.timesync engine.daECS.net.replay
  engine.daECS.scene engine.daECS.utility gameLibs.ecs.phys gameLibs.ecs.anim gameLibs.ecs.gameres
  gameLibs.ecs.scripts.sq gameLibs.ecs.game.generic gameLibs.ecs.game.zones gameLibs.ecs.game.actions
  gameLibs.ecs.rendInst gameLibs.ecs.os gameLibs.ecs.deferToAct engine.daECS.hierarchyTransform gameLibs.ecs.net
  gameLibs.ecs.net.dasevents gameLibs.userSystemInfo gameLibs.statsd 3rdPartyLibs.libb64 gameLibs.ioEventsPoll
  gameLibs.eventLog gameLibs.publicConfigs gameLibs.syncVroms gameLibs.contentUpdater.binarycache
  gameLibs.contentUpdater.utils 1stPartyLibs.sysinfo gameLibs.ecs.console 1stPartyLibs.rapidJsonUtils
  1stPartyLibs.daScriptModules.rapidjson gameLibs.render.denoiser gameLibs.bvh gameLibs.render.rtsm gameLibs.render.rtr
  gameLibs.render.rtao gameLibs.render.ptgi gameLibs.render.quirrel gameLibs.render.objectMotionBlur
  gameLibs.render.indoorProbes gameLibs.gpuMemoryDumper gameLibs.resourcePool gameLibs.render.autoGraphics
  gameLibs.gpuMemoryInspector gameLibs.ecs.debug # the ECS debug tools (their pull: ecsDebug)
)
if(DAGOR_GAME_RENDERER)
  list(APPEND deps gameLibs.render.animatedSplashScreen gameLibs.render.cameraInCamera)
  list(APPEND pulls framework_cameraInCamera_pull)
else()
  list(APPEND deps gameLibs.render.animatedSplashScreen.stub)
endif()
# the camera manager, ambient occlusion and multi-line debug labels
if(DAGOR_GAME_RENDERER)
  list(APPEND deps gameLibs.cameraManager gameLibs.render.ambientOcclusion)
  list(APPEND pulls framework_cameraManager_pull)
else()
  list(APPEND deps gameLibs.cameraManager.stub)
endif()
list(APPEND deps gameLibs.render.debugMultiTextLabels)

if(DAGOR_GAME_DNG_INPUT)
  list(APPEND deps gameLibs.daInput gameLibs.ecs.input)
  _dng_deps("${imgui}" gameLibs.imguiInput ELSE gameLibs.imguiInput.stub)
else()
  list(APPEND deps gameLibs.imguiInput.stub gameLibs.daInput.stub)
endif()
if(DAGOR_GAME_OVERLAY_UI)
  list(APPEND deps gameLibs.quirrel.sqEventBus gameLibs.quirrel.ecsComputed)
endif()

if(CMAKE_SYSTEM_NAME MATCHES "^(Linux|Windows)$")
  list(APPEND deps gameLibs.webui.websocket)
else()
  list(APPEND deps gameLibs.webui.websocket.stub)
endif()
_dng_deps("${desktop_dev}" 3rdPartyLibs.mongoose)
set(shader_editors gameLibs.webui.plugins.shaderEditors.stub)
if(DAGOR_GAME_RENDERER AND WIN32)
  set(shader_editors gameLibs.webui.plugins.shaderEditors)
endif()
_dng_deps("${webui}" gameLibs.webui gameLibs.webui.plugins.ecsviewer gameLibs.webui.plugins.editorCurves
  gameLibs.webui.plugins.colorpicker gameLibs.webui.plugins.webView gameLibs.webui.plugins.rendinstColors
  ${shader_editors} ELSE gameLibs.webui.stub gameLibs.webui.plugins.shaderEditors.stub)

if(DAGOR_GAME_FX)
  list(APPEND deps engine.libFx gameLibs.daFx gameLibs.effectManager)
endif()
_dng_deps("${editor}" gameLibs.daEditorE gameLibs.dasModules.daEditor)
if(DAGOR_GAME_EMBEDDED_BROWSER)
  list(APPEND deps gameLibs.daRg.browser gameLibs.webBrowserHelper gameLibs.quirrel.sqWebBrowser)
else()
  list(APPEND deps gameLibs.daRg.browser.stub gameLibs.quirrel.sqWebBrowser.stub)
endif()

if(DAGOR_GAME_RENDERER)
  list(APPEND deps 3rdPartyLibs.image.avif 3rdPartyLibs.image.jpeg-6b 3rdPartyLibs.image.libpng-1.4.22
    3rdPartyLibs.image.psdRead 3rdPartyLibs.image.tinyexr-1.0.8 engine.screenShotSystem gameLibs.aviWriter
    engine.videoPlayer gameLibs.videoEncoder gameLibs.profileEventsGUI gameLibs.render gameLibs.render.occlusion
    gameLibs.collisionOccluders gameLibs.render.outline gameLibs.render.camouflage gameLibs.render.tracer
    gameLibs.render.cables gameLibs.render.genericLUT gameLibs.render.rainX7 gameLibs.render.hdrRender
    gameLibs.render.heatHaze gameLibs.render.lruCollision gameLibs.render.wind gameLibs.render.waterRipples
    gameLibs.render.wakePs gameLibs.render.foam gameLibs.render.texDebug gameLibs.render.fastGrassBaker
    gameLibs.render.levelProfiler gameLibs.render.voxelizationTarget gameLibs.GIWindows gameLibs.daGI2
    gameLibs.voxelizedMedia gameLibs.ecs.render gameLibs.ecs.render.weather_effects gameLibs.ecs.camera
    gameLibs.ecs.weather gameLibs.ecs.lights gameLibs.daFracture.render gameLibs.rendInst.riFx gameLibs.projectiveDecals
    gameLibs.billboardDecals gameLibs.render.dof gameLibs.render.volumetricLights gameLibs.render.enviCover
    gameLibs.render.nodeBasedShader gameLibs.nodeBasedShaderManager gameLibs.fpsProfiler gameLibs.render.upscale
    gameLibs.textureUtil gameLibs.render.daFrameGraph # with its daScript and daECS integration in game trees (DAGOR_DAFG_FEATURES)
    gameLibs.render.metronome gameLibs.das.daFrameGraph gameLibs.render.resourceSlot gameLibs.render.shaderCacheWarmup
    gameLibs.render.antialiasing gameLibs.dasModules.shaders gameLibs.dasModules.render gameLibs.dasModules.stdGui
    gameLibs.dasModules.camera gameLibs.dasModules.projectiveDecals gameLibs.render.deviceResetTelemetry
    gameLibs.render.psoCacheLoader gameLibs.daSkies2 gameLibs.daSkies2.debug gameLibs.iblCube)
  list(APPEND pulls daSkies2_clouds_field_debug_pull iblCube_ecs_pull_ref)
else()
  list(APPEND deps gameLibs.gamePhys.phys.destrRenderStub gameLibs.daFracture.renderStub gameLibs.render.cables.stub
    gameLibs.rendInst.riFx.stub gameLibs.render.hdrRender.stub gameLibs.render.enviCover.stub
    gameLibs.render.volumetricLights.stub gameLibs.render.nodeBasedShader.stub gameLibs.render.antialiasing.stub)
endif()
if(DAGOR_DAS_AOT)
  list(APPEND pulls daslib_DAS_pull_AOT)
endif()
_dng_deps("${imgui}" 1stPartyLibs.daScript.modules.dasImgui gameLibs.dasModules.imgui gameLibs.consoleWindow ELSE
  gameLibs.consoleWindow.consoleWindowStub)
if(DAGOR_DAS_AOT AND NOT imgui STREQUAL "0")
  list(APPEND pulls "$<${imgui}:daslib_imgui_DAS_pull_AOT>") # daslib's imgui modules
endif()
list(APPEND deps engine.imgui.util 1stPartyLibs.daScript.modules.dasQuirrel gameLibs.vr)
set(std_dlg 0)
if(DAGOR_GAME_RENDERER AND WIN32)
  set(std_dlg "${dev}")
endif()
_dng_deps("${std_dlg}" 1stPartyLibs.daScript.modules.dasStdDlg ELSE 1stPartyLibs.daScript.modules.dasStdDlg.stub)
list(APPEND deps 3rdPartyLibs.openssl-3.x)

if(DAGOR_DEDICATED)
  # headless
  list(APPEND deps engine.drv.hid_nulldrv)
  if(LINUX)
    list(APPEND deps engine.osApiWrappers.messageBox.stub engine.workCycle.stub)
  endif()
  list(APPEND deps gameLibs.quirrel.frp gameLibs.forceFeedback.stub gameLibs.consoleKeyBindings.consoleKeyBindingsStub
    gameLibs.daRg.stub engine.drv.drv3d_pc_multi # the stub (DAGOR_D3D_DRIVERS)
  )
else()
  list(APPEND deps engine.osApiWrappers.messageBox commonFx.commonFxGame gameLibs.daRg gameLibs.dasModules.clientNet
    gameLibs.dasModules.auth gameLibs.forceFeedback engine.drv.drv3d_pc_multi # the platform's drivers (DAGOR_D3D_DRIVERS)
  )
  _dng_deps("${DAGOR_GAME_CONSOLE}" gameLibs.visualConsole ELSE gameLibs.visualConsole.visconstub)
  set(key_bindings 0)
  if(CMAKE_SYSTEM_NAME MATCHES "^(Linux|Windows)$")
    set(key_bindings "$<AND:${DAGOR_GAME_CONSOLE},${dev}>")
  endif()
  _dng_deps("${key_bindings}" gameLibs.consoleKeyBindings ELSE gameLibs.consoleKeyBindings.consoleKeyBindingsStub)
  if(WIN32)
    set(system_libs System::ws2_32 System::shlwapi)
  elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  elseif(NOT LINUX)
    message(FATAL_ERROR "daNetGame has no ${DAGOR_PLATFORM} client: its platform libraries (gameLibs/ios, "
      "gameLibs/android: accounts, billing, the platform's services) are not part of the engine's sources")
  endif()
  # keyboard, mouse and game controllers
  list(APPEND deps engine.drv.hid_keyboard engine.drv.hid_mouse)
  if(WIN32)
    list(APPEND deps engine.drv.hid_joystick engine.drv.hid_gamepad_xinput engine.drv.hid_dinput engine.drv.hid_dspad_pc)
  elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
    list(APPEND deps engine.drv.hid_joystick_osx)
  else()
    list(APPEND deps engine.drv.hid_joystick_linux engine.drv.hid_dspad_pc)
  endif()
endif()
if(WIN32 AND DAGOR_ARCH STREQUAL "x86_64" AND NOT DAGOR_DEDICATED)
  list(APPEND deps gameLibs.nvCacheTracker)
else()
  list(APPEND deps gameLibs.nvCacheTracker.stub)
endif()

# sound: FMOD Studio's (DAGOR_GAME_SOUND), and the sound events of the network (DAGOR_GAME_SOUND_NET)
if(DAGOR_GAME_SOUND)
  if(NOT TARGET gameLibs.soundSystem)
    message(FATAL_ERROR "daNetGame: DAGOR_GAME_SOUND needs the FMOD Studio API (\"FMOD Engine\" at fmod.com): install "
                        "it or set FMOD_ROOT (prog/cmake/find/FindFMOD.cmake)")
  endif()
  list(APPEND deps gameLibs.soundSystem gameLibs.soundSystem.quirrel gameLibs.ecs.sound gameLibs.daRg.soundSystem
    gameLibs.dasModules.sound)
else()
  list(APPEND deps gameLibs.soundSystem.stub gameLibs.soundSystem.quirrel.stub gameLibs.ecs.sound.stub)
endif()
if(DAGOR_GAME_SOUND_NET)
  list(APPEND deps gameLibs.dasModules.sound.common)
endif()
if(DAGOR_CRASHPAD)
  list(APPEND deps gameLibs.breakpad.crashpad)
else()
  list(APPEND deps "$<IF:${DAGOR_BREAKPAD_CONFIGS},gameLibs.breakpad.binder,gameLibs.breakpad.stub>")
endif()

# --- generated code --------------------------------------------------------------------------------------------------
set(gen "${CMAKE_CURRENT_BINARY_DIR}/gen")
if(DAGOR_GAME_RENDERER)
  file(CONFIGURE OUTPUT "${gen}/iblCubePullRef.cpp" CONTENT
    "#include <stddef.h>\nextern const size_t ecs_pull_iblCube;\nsize_t iblCube_ecs_pull_ref = (size_t)(&ecs_pull_iblCube);\n")
  set(generated "${gen}/iblCubePullRef.cpp")
else()
  # daSkies' clouds rain map pull, which a renderless build has not
  file(CONFIGURE OUTPUT "${gen}/daSkies2PullStub.cpp" CONTENT
    "#include <stddef.h>\nextern const size_t ecs_pull_cloudsRainMap = (size_t)(&ecs_pull_cloudsRainMap);\n")
  set(generated "${gen}/daSkies2PullStub.cpp")
endif()
# the daScript pulls of the client and the server: the tree's own is its daScript's (DAS_PULL), the other's is 0
if(DAGOR_DEDICATED)
  set(das_pull daNetGame_server_DAS_pull_AOT)
  set(text "size_t daNetGame_client_DAS_pull_AOT = 0;\n")
else()
  set(das_pull daNetGame_client_DAS_pull_AOT)
  set(text "size_t daNetGame_server_DAS_pull_AOT = 0;\n")
endif()
if(DAGOR_DAS_AOT)
  string(APPEND text "bool NEED_DAS_AOT_COMPILE = true;\n")
else()
  string(APPEND text "bool NEED_DAS_AOT_COMPILE = false;\n")
endif()
file(CONFIGURE OUTPUT "${gen}/dasAot.cpp" CONTENT "#include <stddef.h>\n${text}")
list(APPEND generated "${gen}/dasAot.cpp")

# --- the library -----------------------------------------------------------------------------------------------------
# the precompiled header (Windows, Dev and Dbg only); not on Apple platforms, whose SDK has no <malloc.h>
set(pch)
if(CMAKE_SYSTEM_NAME MATCHES "^(Linux|Windows)$")
  set(pch precompile.h)
endif()
dagor_add_target(NAME daNetGame STATIC
  FILES_CMAKE daNetGame_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_DNG_INCLUDES} ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/engine ${DAGOR_PROG_DIR}/gameLibs ${DAGOR_PROG_DIR}/gameLibs/render/animatedSplashScreen/public_api
  COMPILE_DEFINITIONS PRIVATE DISABLE_SYNC_DEBUG # the fork has no gameLibs/syncDebug
  COMPILE_OPTIONS PRIVATE ${DAGOR_DNG_OPTIONS}
  BUILD_DEPENDENCIES
    PUBLIC ${system_libs}
    PRIVATE Dagor::Quirrel ${deps} Dagor::Phys
  PCH ${pch}
  DAS_PULL ${das_pull}
  PROPERTIES DAGOR_FRAME_LIMIT 262144
)
target_sources(daNetGame PRIVATE ${generated})
# the crash report sender next to the game (DAGOR_BREAKPAD_SUBMISSION)
if(DAGOR_BREAKPAD_SUBMISSION AND NOT DAGOR_CRASHPAD)
  if(NOT TARGET bpreport)
    message(FATAL_ERROR "DAGOR_BREAKPAD_SUBMISSION: bpreport (gameLibs/breakpad/sender) is not built for ${DAGOR_PLATFORM}")
  endif()
  add_dependencies(daNetGame bpreport)
  set_property(TARGET daNetGame APPEND PROPERTY INTERFACE_DAGOR_RUNTIME_FILES ".|$<TARGET_FILE:bpreport>")
endif()
# the pull of the framework's entity systems
_dagor_es_pulls(daNetGame es_pulls)
_dagor_pull_file(daNetGame "${gen}/daNetGame_es_pull.cpp" ECS framework_es_pulls ${es_pulls} ecsDebug)
set_property(TARGET daNetGame APPEND PROPERTY INTERFACE_DAGOR_GAME_PULLS ${pulls})
