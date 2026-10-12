# OS API wrappers: files, threads, sync, sockets, dynamic libs, debug output, clipboard, message box.
#
# On Linux the window title and clipboard come from engine/osApiWrappers/linuxGUI in programs with a GUI and from
# stubs otherwise. A program chooses with the DAGOR_LINUX_GUI target property (dagor_add_executable(... PROPERTIES
# DAGOR_LINUX_GUI ON)), or gets ON from a library that sets INTERFACE_DAGOR_LINUX_GUI (the Vulkan driver); see
# dagor_add_link_choice().
add_subdirectory(linuxGUI)
add_subdirectory(messageBox)

set(sources
  critsec.cpp
  timedCritsec.cpp
  limBufWriter.cpp
  dbgStrFmt.cpp
  symHlp.cpp
  basePath.cpp
  basePathMgr.cpp
  namedMounts.cpp
  syncFileIo.cpp
  localCmp.cpp
  simplifyFname.cpp
  directoryService.cpp
  directoryUtils.cpp
  getRealFname.cpp
  wndProcComponent.cpp
  miscApi.cpp
  progGlobals.cpp
  setThreadName.cpp
  ip2str.cpp
  vromfs.cpp
  unicode.cpp
  cpuJobs.cpp
  threads.cpp
  fileIoErr.cpp
  events.cpp
  spinlock.cpp
  rwlock.cpp
  globalMutex.cpp
  sharedMem.cpp
  mmap.cpp
  virtualMem.cpp
  sockets.cpp
  wildcards.cpp
  findFilePosix.cpp
  shellExecute.cpp
  singleProcessChecker.cpp
  directoryWatch.cpp
  cpuFeatures.cpp
  versionQuery.cpp
  winVersionQuery.cpp
)
if(WIN32 AND DAGOR_ARCH STREQUAL "x86_64")
  list(APPEND sources fastStackCapture.cpp)
else()
  list(APPEND sources fastStackCaptureStub.cpp)
endif()

set(includes ${DAGOR_PROG_DIR}/engine/sharedInclude)
set(deps)
set(libs)
set(options)
if(DAGOR_SYNC_ASYNC_READ)
  set(posix_async_read posix/posixSyncAsyncRead.cpp)
elseif(DAGOR_SANITIZE STREQUAL "thread")
  set(posix_async_read posix/posixThreadAsyncRead.cpp)
else()
  set(posix_async_read posix/posixAIOAsyncRead.cpp)
endif()

if(WIN32)
  list(APPEND sources dbgStr.cpp findFile.cpp winSetTitle.cpp stackHlpFill.cpp stackHlpGet.cpp addressWaitWinApi.cpp
    winClipboard.cpp winHwExceptUtils.cpp winXStateFeatures.cpp winapiAsyncRead.cpp dynLib.cpp)
  list(APPEND deps engine.osApiWrappers.messageBox)
  list(APPEND libs System::shell32 System::version)
elseif(APPLE)
  if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
    list(APPEND sources macosx/mac_shell.mm)
    list(APPEND deps engine.osApiWrappers.messageBox)
  elseif(IOS)
    list(APPEND sources ios/iOS_shell.mm ios/iOS_windowScene.mm)
    list(APPEND deps engine.osApiWrappers.messageBox)
  else()
    list(APPEND sources ios/iOS_shell.mm ios/iOS_windowScene.mm tvos/tvOS_storage.mm tvos/tvOS_appstore.mm tvos/tvOS_callbacks.mm
      tvos/tvOS_logimpl.mm tvos/eventviewcontroller.mm tvos/gamecenterview.mm tvos/inetview.mm
      tvos/matchcontroller.mm tvos/storekitview.mm)
    list(APPEND deps engine.osApiWrappers.messageBox.stub)
  endif()
  list(APPEND sources stackHlpFill.cpp stackHlpGet.cpp macosx/macDbgStr.mm macosx/macSetTitle.mm
    macosx/macClipboard.mm macosx/addressWaitOsSync.cpp convertUTF.cpp dynLib.cpp ${posix_async_read})
  list(APPEND options -Wno-error)
elseif(CMAKE_SYSTEM_NAME MATCHES "^(Android|Linux)$")
  list(APPEND sources dbgStr.cpp stackHlpFill.cpp stackHlpGet.cpp dynLib.cpp convertUTF.cpp linux/addressWaitFutex.cpp)
  if(ANDROID)
    list(APPEND sources posix/posixThreadAsyncRead.cpp android/androidClipboard.cpp)
    list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/libunwind/include)
    list(APPEND deps engine.osApiWrappers.messageBox.stub 3rdPartyLibs.libunwind)
  else()
    list(APPEND sources ${posix_async_read})
    # the GUI or the stubs, by the DAGOR_LINUX_GUI property of the program this ends up in
    dagor_add_library(engine.osApiWrappers.noGUI linux/linuxSetTitleStub.cpp linux/linuxClipboardStub.cpp)
    target_include_directories(engine.osApiWrappers.noGUI PRIVATE ${includes})
    target_compile_definitions(engine.osApiWrappers.noGUI PRIVATE __B_KERNEL_LIB)
    dagor_add_link_choice(engine.osApiWrappers.linuxShell PROPERTY DAGOR_LINUX_GUI
      ON engine.osApiWrappers.linuxGUI OFF engine.osApiWrappers.noGUI)
    list(APPEND deps engine.osApiWrappers.linuxShell)
  endif()
endif()

dagor_add_library(engine.osApiWrappers ${sources})
target_include_directories(engine.osApiWrappers PRIVATE ${includes})
target_compile_definitions(engine.osApiWrappers PRIVATE __B_KERNEL_LIB)
target_compile_options(engine.osApiWrappers PRIVATE ${options})
target_link_libraries(engine.osApiWrappers PRIVATE ${deps})
target_link_libraries(engine.osApiWrappers PUBLIC ${libs})
