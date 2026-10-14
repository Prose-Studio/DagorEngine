# dargbox, the daRg sandbox: runs daRg UI scripts with live reload (the dargbox tree), in tools/dargbox/<platform>-<arch>
# (on Android its APK and on iOS its app bundle in tools/dargbox/<platform>, on macOS the app bundle in tools/dargbox),
# with the tree's 3d drivers and, on Windows, VR (DAGOR_VR)
set(out ${DAGOR_ENGINE_ROOT}/tools/dargbox/${DAGOR_PLATFORM}-${DAGOR_ARCH})
if(ANDROID OR IOS)
  set(out ${DAGOR_ENGINE_ROOT}/tools/dargbox/${DAGOR_PLATFORM})
elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  set(out ${DAGOR_ENGINE_ROOT}/tools/dargbox)
endif()
# the memory debug checks on Windows
set(memory engine.memory)
if(WIN32)
  set(memory engine.memory.default.dbg)
endif()
set(deps
  engine.osApiWrappers engine.kernel ${memory} engine.ioSys engine.startup engine.baseUtil engine.coreUtil engine.math
  engine.lib3d engine.image engine.shaders engine.workCycle engine.guiBase engine.libFx engine.gameRes
  commonFx.commonFxGame gameLibs.vr gameLibs.webui gameLibs.daRg gameLibs.dasModules.render gameLibs.dasModules.shaders
  gameLibs.dasModules.stdGui gameLibs.folders gameLibs.visualConsole gameLibs.render gameLibs.webvromfs
  gameLibs.ioEventsPoll gameLibs.quirrel.bindQuirrelEx gameLibs.quirrel.http gameLibs.quirrel.sqConsole
  gameLibs.quirrel.base64 gameLibs.quirrel.sqDebugger gameLibs.quirrel.nestdb gameLibs.quirrel.udp
  gameLibs.quirrel.sqDataCache gameLibs.quirrel.asyncRuntime engine.perfMon engine.consoleProc tools.libTools.util
  tools.libTools.grsCurView 3rdPartyLibs.image.libpng-1.4.22 3rdPartyLibs.image.jpeg-6b 3rdPartyLibs.image.avif
  3rdPartyLibs.image.psdRead 1stPartyLibs.daScript
  engine.drv.drv3d_pc_multi
)
set(options)
set(properties DAGOR_LINUX_GUI ON)
if(WIN32)
  list(APPEND deps engine.drv.hid_mouse engine.drv.hid_keyboard engine.drv.hid_joystick engine.drv.hid_dinput
    engine.drv.hid_gamepad_xinput engine.drv.hid_dspad_pc gameLibs.quirrel.win_registry)
  list(APPEND properties DAGOR_VR ON) # OpenXR
elseif(LINUX)
  list(APPEND deps engine.drv.hid_mouse engine.drv.hid_keyboard engine.drv.hid_joystick_linux
    engine.osApiWrappers.messageBox)
elseif(ANDROID)
  list(APPEND deps engine.drv.hid_android engine.drv.hid_nulldrv)
elseif(IOS)
  # the iOS main needs the system info (memory warnings) and the haptics; daFx needs ImGui (its stub)
  list(APPEND deps engine.drv.hid_iOS engine.drv.hid_nulldrv engine.imgui.stub gameLibs.userSystemInfo
    System::AVFoundation System::CoreHaptics)
elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND deps engine.imgui.stub engine.drv.hid_mouse engine.drv.hid_keyboard engine.drv.hid_joystick_osx
    engine.drv.hid_nulldrv engine.osApiWrappers.messageBox)
  set(options -Wno-deprecated-declarations)
endif()
if(APPLE AND NOT IOS)
  list(APPEND deps System::CoreAudio System::AudioUnit)
endif()

dagor_add_target(NAME dargbox EXECUTABLE APPLICATION LAX
  OUTPUT_DIRECTORY ${out}
  FILES_CMAKE dargbox_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
    ${DAGOR_PROG_DIR}/gameLibs/daRg ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/engine/drv
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE ${deps} Dagor::Quirrel
  PROPERTIES ${properties}
)
# its content in tools/dargbox: the shaders of the 3d drivers the platform's dargbox renders with, and the vromfs of its
# scripts (the iOS app bundle carries no content)
set(shaders ${DAGOR_ENGINE_ROOT}/tools/dargbox/shaders)
if(WIN32)
  dagor_add_shaders(dargbox-shaders-dx11 COMPILER dsc2-hlsl11 BLK shaders/shaders_dx11.blk OUTPUT ${shaders}/game)
  dagor_add_shaders(dargbox-shaders-dx12 COMPILER dsc2-dx12 BLK shaders/shaders_dx12.blk OUTPUT ${shaders}/gameDX12)
  dagor_build_by_default(dargbox-shaders-dx11 dargbox-shaders-dx12)
endif()
if(CMAKE_SYSTEM_NAME MATCHES "^(Linux|Windows|Android)$")
  dagor_add_shaders(dargbox-shaders-spirv COMPILER dsc2-spirv BLK shaders/shaders_spirv.blk OUTPUT ${shaders}/gameSpirV)
  dagor_build_by_default(dargbox-shaders-spirv)
endif()
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  dagor_add_shaders(dargbox-shaders-metal COMPILER dsc2-metal BLK shaders/shaders_metal.blk OUTPUT ${shaders}/gameMTL)
  dagor_build_by_default(dargbox-shaders-metal)
endif()
if(NOT IOS)
  dagor_add_content_step(dargbox-vromfs TOOL vromfsPacker ARGS darg.vromfs.blk -platform:PC -quiet
    COMMENT "dargbox's vromfs")
  dagor_build_by_default(dargbox-vromfs)
endif()

if(APPLE)
  dagor_apple_bundle(dargbox NAME dargbox ID com.gaijinent.dargbox)
elseif(ANDROID)
  # the APK: the activities of platform/android.bundle, the vromfs of the scripts and of the platform's settings, the
  # Vulkan shaders
  dagor_add_content_step(dargbox-vromfs-android TOOL vromfsPacker ARGS android.vromfs.blk -platform:and -quiet
    COMMENT "dargbox's Android vromfs")
  set(java platform/android.bundle/src)
  set(dargbox_dir ${DAGOR_ENGINE_ROOT}/tools/dargbox)
  dagor_android_apk(dargbox ID com.gaijinent.dargbox ACTIVITY com.gaijinent.dargbox.Dargbox LABEL Dargbox
    PERMISSIONS INTERNET ACCESS_NETWORK_STATE ACCESS_WIFI_STATE VIBRATE
    JAVA ${java}/Dargbox.java ${java}/DagorCommonActivity.java ${java}/DagorBaseActivity.java
    ASSETS
      "dargbox.vromfs.bin|${dargbox_dir}/dargbox.vromfs.bin" "android.vromfs.bin|${dargbox_dir}/android.vromfs.bin"
      "shaders/gameSpirV.ps50.shdump.bin|${shaders}/gameSpirV.ps50.shdump.bin"
    DEPENDS dargbox-vromfs dargbox-vromfs-android dargbox-shaders-spirv)
  dagor_build_by_default(dargbox.apk)
endif()
