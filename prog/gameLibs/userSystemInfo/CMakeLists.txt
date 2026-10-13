# The user system info (no Steam or Epic store libraries in the fork; on iOS its network state needs gameLibs/ios, which
# is not in the sources)
list(APPEND deps 3rdPartyLibs.openssl-3.x)
if(WIN32)
  list(APPEND libs System::iphlpapi System::rpcrt4 System::wbemuuid)
endif()
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND libs System::DiskArbitration System::IOKit)
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
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude/compressionUtils
    ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include ${DAGOR_PROG_DIR}/3rdPartyLibs ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/tools/sharedInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES
    PUBLIC ${libs}
    PRIVATE ${deps}
)
