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

# the hardware breakpoints (Windows x64, through minhook) are not in Rel; with DAGOR_FORCE_LOGS Rel encrypts its logs
set(dir "${CMAKE_CURRENT_LIST_DIR}")
if(WIN32 AND DAGOR_ARCH STREQUAL "x86_64")
  list(APPEND FILES "$<${not_rel}:${dir}/dagorHwBreakpoint.cpp>")
else()
  list(APPEND FILES "$<${not_rel}:${dir}/stub/dagorHwBreakpoint.cpp>")
endif()
if(DAGOR_FORCE_LOGS)
  list(APPEND FILES "$<$<CONFIG:Rel>:${dir}/def_logCryptKey.cpp>")
endif()
