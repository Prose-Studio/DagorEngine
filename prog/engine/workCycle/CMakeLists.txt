# The work cycle: the main loop, timing, input device init, the console in Dev and Dbg
add_subdirectory(stub)

set(sources
  gameSetts.cpp
  gameActRate.cpp
  gameSceneSelect.cpp
  gameSceneRenderer.cpp
  resetSpentTime.cpp
  workCycle.cpp
  workCyclePerf.cpp
  initVideo.cpp
  initNullJoystick.cpp
  initNullKeyb.cpp
  initNullMouse.cpp
  commonStart.cpp
  mainWndProc.cpp
)
if(WIN32)
  list(APPEND sources idleCycle.cpp)
endif()
if(WIN32)
  list(APPEND sources initJoystick.cpp initJoystickXInput.cpp initKeybWin.cpp initMouseWin.cpp)
endif()
if(WIN32)
  list(APPEND sources windows/threadedWindow.cpp)
endif()
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND sources macosx/macIdleCycle.mm initKeybWin.cpp initMouseWin.cpp)
endif()
if(IOS)
  list(APPEND sources macosx/iosIdleCycle.mm initJoystick.cpp initKeybWin.cpp initMouseWin.cpp)
endif()
if(CMAKE_SYSTEM_NAME STREQUAL "tvOS")
  list(APPEND sources macosx/iosIdleCycle.mm macosx/initRemoteControl.mm initKeybWin.cpp initMouseWin.cpp)
endif()
if(LINUX)
  list(APPEND sources idleCycle.cpp initKeybWin.cpp initMouseWin.cpp)
  # the Linux GUI layer comes with engine/osApiWrappers in the programs with DAGOR_LINUX_GUI
endif()
if(ANDROID)
  list(APPEND sources idleCycle.cpp initJoystick.cpp initKeybWin.cpp initMouseWin.cpp)
endif()
set(includes ${DAGOR_PROG_DIR}/engine/sharedInclude)
set(deps engine.perfMon engine.lowLatency engine.coreUtil)
list(APPEND deps "$<$<CONFIG:Dev,Dbg>:engine.consoleProc>")
list(APPEND deps engine.drv.vr_device)

dagor_add_library(engine.workCycle ${sources})
target_include_directories(engine.workCycle PRIVATE ${includes})
target_link_libraries(engine.workCycle PRIVATE ${deps})
