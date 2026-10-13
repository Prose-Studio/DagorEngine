set(FILES
  fatalerr.cpp
  kernelGlobalSetting.cpp
  globalVars/occlusion_map.cpp
  globalVars/hdrMode.cpp
  cdebug.c
  debugDumpStack.cpp
  logimpl.cpp
  writeStream.cpp
  cpuControl.cpp
  perfTimer.cpp
)

# the hardware breakpoints (Windows x64, through minhook) are not in Rel: a source of every configuration (the Xcode
# generator takes no per-configuration ones) that compiles them where DAGOR_DBGLEVEL is not 0
set(dir "${CMAKE_CURRENT_LIST_DIR}")
set(hw_breakpoint "${dir}/stub/dagorHwBreakpoint.cpp")
if(WIN32 AND DAGOR_ARCH STREQUAL "x86_64")
  set(hw_breakpoint "${dir}/dagorHwBreakpoint.cpp")
endif()
file(CONFIGURE OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/gen/hwBreakpoint.cpp"
  CONTENT "#if DAGOR_DBGLEVEL != 0
#include \"${hw_breakpoint}\"
#endif
")
list(APPEND FILES "${CMAKE_CURRENT_BINARY_DIR}/gen/hwBreakpoint.cpp")
# with DAGOR_FORCE_LOGS the release logs are encrypted with this key unless the game has its own (only what references
# it pulls it from the library)
if(DAGOR_FORCE_LOGS)
  list(APPEND FILES ${dir}/def_logCryptKey.cpp)
endif()
