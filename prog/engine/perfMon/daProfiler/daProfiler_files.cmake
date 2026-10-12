set(FILES
  daProfiler.cpp
  daProfilerPlugins.cpp
  daProfilePageAllocator.cpp
  daProfilerOOL.cpp
  daProfilerThreads.cpp
  daProfilerVSDump.cpp
  daProfilerMessageServer.cpp
  daProfilerDefaultMessages.cpp
  daProfilerDumpServer.cpp
  daProfilerDescriptions.cpp
  daProfilerDataDescriptions.cpp
  daProfilerSampling.cpp
  daProfilerDumpHier.cpp
  daProfilerSaveDump.cpp
  daProfilerPrepareDump.cpp
  daProfilerPlatform.cpp
  daProfilerPlatformGPU.cpp
  daProfilerFileDump.cpp
  daProfilerLogDump.cpp
  daProfilerNetServer.cpp
  daProfilerUserSettings.cpp
  daProfilerUserSettingsDump.cpp
  daProfilerSymbolsCache.cpp
)
if(WIN32)
  list(APPEND FILES stackUnwinder/unwindStackWin.cpp)
elseif(ANDROID)
  list(APPEND FILES stackUnwinder/unwindStackAndroid.cpp)
elseif(APPLE)
  list(APPEND FILES stackUnwinder/unwindStackMac.cpp)
else()
  list(APPEND FILES stackUnwinder/unwindStackDagor.cpp)
endif()
