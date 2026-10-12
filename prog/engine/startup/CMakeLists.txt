# Program startup helpers (message box crash report on Windows)
set(sources
  checkCpuid.cpp
  globals.cpp
  globals3d.cpp
  initCrt.cpp
  loadSettings.cpp
  purgeLogs.cpp
  applyCmdline.cpp
  mbReport.cpp
  inpDevClsDrv.cpp
  regCommonGameTex.cpp
  regCommonToolTex.cpp
  regTexCreateDds.cpp
  regTexCreateLoadable.cpp
  setDefFileTF.cpp
  setDefSymTF.cpp
  splashScreen_stub.cpp
  memReport.cpp
  memReportRef.cpp
  joy_data.cpp
  kbd_data.cpp
  ms_data.cpp
)
if(WIN32)
  list(APPEND sources mbWinReport.cpp)
endif()
set(includes ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/3rdPartyLibs)
if(DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  set(deps engine.memory.rtlOverride)
endif()
list(APPEND deps 3rdPartyLibs.eastl)

dagor_add_library(engine.startup LAX ${sources})
target_include_directories(engine.startup PRIVATE ${includes})
target_link_libraries(engine.startup PRIVATE ${deps})
