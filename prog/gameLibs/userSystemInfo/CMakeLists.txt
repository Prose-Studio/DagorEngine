# Ported from prog/gameLibs/userSystemInfo/jamfile (jam2cmake/skeleton.py; no Steam or Epic store libraries in the fork)
set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/compressionUtils
  ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  ${DAGOR_PROG_DIR}/3rdPartyLibs
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/tools/sharedInclude
)
set(sources systemInfo.cpp dumpSysInfo.cpp userSystemInfo.cpp uuidgen.cpp redistInfo.cpp)
list(APPEND sources systemInfo_stubext.cpp) # the fork has no systemInfo_private.cpp
list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include)
list(APPEND deps 3rdPartyLibs.openssl-3.x)
if(WIN32)
  list(APPEND libs System::iphlpapi System::rpcrt4 System::wbemuuid)
endif()
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND sources macosx_spec.mm)
  list(APPEND libs "$<LINK_LIBRARY:FRAMEWORK,DiskArbitration>" "$<LINK_LIBRARY:FRAMEWORK,IOKit>")
endif()
if(IOS)
  list(APPEND deps gameLibs/ios/net_reachability)
  list(APPEND sources ios_spec.mm)
endif()
if(CMAKE_SYSTEM_NAME MATCHES "^(Android|Darwin|Linux|Windows)$" AND NOT DAGOR_ARCH STREQUAL "e2k")
  list(APPEND deps 3rdPartyLibs.cpu_features)
  list(APPEND defines USE_CPU_FEATURES)
endif()
list(APPEND deps 3rdPartyLibs.hash engine.drv.vr_device)
if(CMAKE_SYSTEM_NAME MATCHES "^(Android|Darwin|Linux|Windows|iOS)$")
  list(APPEND deps gameLibs.folders)
endif()

dagor_add_library(gameLibs.userSystemInfo LAX ${sources})
target_include_directories(gameLibs.userSystemInfo PRIVATE ${includes})
target_compile_definitions(gameLibs.userSystemInfo PRIVATE ${defines})
target_link_libraries(gameLibs.userSystemInfo PRIVATE ${deps})
target_link_libraries(gameLibs.userSystemInfo PUBLIC ${libs})
