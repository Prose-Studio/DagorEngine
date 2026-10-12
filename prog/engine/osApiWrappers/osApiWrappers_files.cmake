set(FILES
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
  list(APPEND FILES fastStackCapture.cpp)
else()
  list(APPEND FILES fastStackCaptureStub.cpp)
endif()
# the asynchronous reads of the POSIX platforms (their _files.cmake)
if(DAGOR_SYNC_ASYNC_READ)
  set(posix_async_read posix/posixSyncAsyncRead.cpp)
elseif(DAGOR_SANITIZE STREQUAL "thread")
  set(posix_async_read posix/posixThreadAsyncRead.cpp)
else()
  set(posix_async_read posix/posixAIOAsyncRead.cpp)
endif()
