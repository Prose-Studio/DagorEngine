# daProfiler: the engine's CPU/GPU profiler with its capture and dump formats
set(includes ${DAGOR_PROG_DIR}/engine/perfMon/daProfiler ${DAGOR_PROG_DIR}/engine/sharedInclude)
if(ANDROID)
  list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/libunwind/include)
  list(APPEND deps 3rdPartyLibs.libunwind)
endif()
set(sources
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
  list(APPEND sources stackUnwinder/unwindStackWin.cpp)
elseif(ANDROID)
  list(APPEND sources stackUnwinder/unwindStackAndroid.cpp)
elseif(APPLE)
  list(APPEND sources stackUnwinder/unwindStackMac.cpp)
else()
  list(APPEND sources stackUnwinder/unwindStackDagor.cpp)
endif()
set(defines __B_KERNEL_LIB)

dagor_add_library(engine.perfMon.daProfiler ${sources})
target_include_directories(engine.perfMon.daProfiler PRIVATE ${includes})
target_compile_definitions(engine.perfMon.daProfiler PRIVATE ${defines})
target_link_libraries(engine.perfMon.daProfiler PRIVATE ${deps})
