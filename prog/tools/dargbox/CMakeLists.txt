# TODO(jam): LinuxUseGUI = yes ;
# TODO(jam): if $(Config) = rel { ForceLogs = yes ; }
if(CMAKE_SYSTEM_NAME MATCHES "^(Linux|Windows)$")
  # TODO(jam): OutDir = $(OutDir)/$(Platform)-$(PlatformArch) ;
elseif(CMAKE_SYSTEM_NAME MATCHES "^(Android|iOS)$")
  # TODO(jam): OutDir = $(OutDir)/$(Platform) ;
endif()
if(CMAKE_SYSTEM_NAME MATCHES "^(Linux|Windows)$")
  # TODO(jam): UseD3DMulti ?= yes ;
endif()
if(WIN32)
  # TODO(jam): VRDeviceSupport ?= yes ;
endif()
set(deps
  engine.osApiWrappers
  engine.kernel
  engine.memory
  engine.ioSys
  engine.startup
  engine.baseUtil
  engine.coreUtil
  engine.math
  engine.lib3d
  engine.image
  engine.shaders
  engine.workCycle
  engine.guiBase
  engine.libFx
  engine.gameRes
  commonFx.commonFxGame
  gameLibs.vr
  gameLibs.webui
  gameLibs.daRg
  gameLibs.dasModules.render
  gameLibs.dasModules.shaders
  gameLibs.dasModules.stdGui
  gameLibs.folders
  gameLibs.visualConsole
  gameLibs.render
  gameLibs.webvromfs
  gameLibs.ioEventsPoll
  gameLibs.quirrel.bindQuirrelEx
  gameLibs.quirrel.http
  gameLibs.quirrel.sqConsole
  gameLibs.quirrel.base64
  gameLibs.quirrel.sqDebugger
  gameLibs.quirrel.nestdb
  gameLibs.quirrel.udp
  gameLibs.quirrel.sqDataCache
  gameLibs.quirrel.asyncRuntime
  engine.perfMon
  engine.consoleProc
  tools.libTools.util
  tools.libTools.grsCurView
  3rdPartyLibs.image.libpng-1.4.22
  3rdPartyLibs.image.jpeg-6b
  3rdPartyLibs.image.avif
  3rdPartyLibs.image.psdRead
  1stPartyLibs.daScript
)
if(WIN32)
  list(APPEND deps
    engine.drv.hid_mouse
    engine.drv.hid_keyboard
    engine.drv.hid_joystick
    engine.drv.hid_dinput
    engine.drv.hid_gamepad_xinput
    engine.drv.hid_dspad_pc
    gameLibs.quirrel.win_registry
  )
  # TODO(jam): include $(Root)/prog/engine/drv/drv3d_DX12/copy_bundles.jam ;
  # TODO(jam): include $(Root)/prog/engine/drv/drv3d_commonCode/copy_bundles.jam ;
elseif(LINUX)
  list(APPEND deps
    engine.drv.hid_mouse
    engine.drv.hid_keyboard
    engine.drv.hid_joystick_linux
    engine.osApiWrappers.messageBox
  )
elseif(ANDROID)
  list(APPEND deps engine.drv.hid_android engine.drv.hid_nullDrv)
  list(APPEND deps engine.drv.drv3d_vulkan)
  # TODO(jam): BundleCopy =  ;
  set(JavaActivitySrcName Dargbox)
  # TODO(jam): AndroidJavaClass = com.gaijinent.dargbox.Dargbox ;
  # TODO(jam): AndroidAppID = com.gaijinent.dargbox ;
  # TODO(jam): AndroidIcon = ../../samples/Android-testApp-res/icon.png ;
  # TODO(jam): AndroidAppIconName = Dargbox ;
  # TODO(jam): BundleName = dargbox ;
  # TODO(jam): BundleCopy += $(Root)/tools/dargbox/dargbox.vromfs.bin assets/dargbox.vromfs.bin
  #   $(Root)/tools/dargbox/android.vromfs.bin assets/android.vromfs.bin
  #   $(Root)/tools/dargbox/shaders/gameSpirV.ps50.shdump.bin assets/shaders/gameSpirV.ps50.shdump.bin
  #   platform/android.bundle/src/$(JavaActivitySrcName).java
  #   src/com/gaijinent/$(BundleName)/$(JavaActivitySrcName).java
  #   platform/android.bundle/src/DagorCommonActivity.java
  #   src/com/gaijinent/common/DagorCommonActivity.java platform/android.bundle/src/DagorBaseActivity.java
  #   src/com/gaijinent/common/DagorBaseActivity.java ;
elseif(IOS)
  list(APPEND deps engine.drv.hid_iOS engine.drv.hid_nullDrv)
  list(APPEND deps engine.drv.drv3d_Metal)
  list(APPEND link_options -framework AVFoundation)
  # TODO(jam): BundleID = com.gaijinent.dargbox ;
  # TODO(jam): BundleName = dargbox ;
  # TODO(jam): BundlePlist = @$(Root)/prog/_jBuild/iOS/generic.info.plist ../Info.plist ;
  # TODO(jam): BundleCopy =  ;
elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  set(OutDir ${DAGOR_ENGINE_ROOT}/tools/dargbox/dargbox-${DAGOR_ARCH}.app/Contents/MacOS)
  list(APPEND deps
    engine.imgui.stub
    engine.drv.hid_mouse
    engine.drv.hid_keyboard
    engine.drv.hid_joystick_osx
    engine.drv.hid_nulldrv
    engine.osApiWrappers.messageBox
  )
  # TODO(jam): if $(UseStubDriver) = yes { UseProgLibs += engine/drv/drv3d_stub ; } else { UseProgLibs +=
  #   engine/drv/drv3d_Metal ; }
  list(APPEND options -Wno-deprecated-declarations)
  list(APPEND link_options -framework CoreAudio -framework AudioUnit)
  # TODO(jam): Exit unsupported Platform\=$(Platform) for Target\=$(Target) ;
endif()
if(NOT ANDROID)
  # TODO(jam): if $(UseD3DMulti) = yes { UseProgLibs += engine/drv/drv3d_pc_multi ; }
endif()
if(WIN32)
  # TODO(jam): UseMemoryDebugLevel = dbg ;
endif()
# TODO(jam): if $(VRDeviceSupport) = yes { include $(Root)/prog/engine/drv/vr_device/bundle.jam ; }
# TODO(jam): if [ GLOB $(Root)/prog/gameLibs/quirrel/matchingModule : jamfile ] { HaveStunChecker = no ;
#   UseProgLibs += gameLibs/matchingClient gameLibs/quirrel/matchingModule 1stPartyLibs/matching ;
#   CPPopt += -DHAS_MATCHING_MODULE ; }

dagor_add_target(NAME dargbox EXECUTABLE WIN32 LAX OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/dargbox
  FILES_CMAKE dargbox_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
    ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include ${DAGOR_PROG_DIR}/gameLibs/daRg
    ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/engine/drv
  COMPILE_OPTIONS PRIVATE ${options}
  LINK_OPTIONS PRIVATE ${link_options}
  BUILD_DEPENDENCIES PRIVATE ${deps} Dagor::Quirrel
)
