# Ported from prog/gameLibs/userSystemInfo/jamfile (jam2cmake/skeleton.py; no Steam or Epic store libraries in the fork)
set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/compressionUtils
  ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  ${DAGOR_PROG_DIR}/3rdPartyLibs
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/tools/sharedInclude
)
list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include)
list(APPEND deps 3rdPartyLibs.openssl-3.x)
if(WIN32)
  list(APPEND libs System::iphlpapi System::rpcrt4 System::wbemuuid)
endif()
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND libs "$<LINK_LIBRARY:FRAMEWORK,DiskArbitration>" "$<LINK_LIBRARY:FRAMEWORK,IOKit>")
endif()
if(IOS)
  list(APPEND deps gameLibs/ios/net_reachability)
endif()
if(CMAKE_SYSTEM_NAME MATCHES "^(Android|Darwin|Linux|Windows)$" AND NOT DAGOR_ARCH STREQUAL "e2k")
  list(APPEND deps 3rdPartyLibs.cpu_features)
  list(APPEND defines USE_CPU_FEATURES)
endif()
list(APPEND deps 3rdPartyLibs.hash engine.drv.vr_device)
if(CMAKE_SYSTEM_NAME MATCHES "^(Android|Darwin|Linux|Windows|iOS)$")
  list(APPEND deps gameLibs.folders)
endif()

dagor_add_target(NAME gameLibs.userSystemInfo STATIC LAX
  FILES_CMAKE userSystemInfo_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES
    PUBLIC ${libs}
    PRIVATE ${deps}
)
