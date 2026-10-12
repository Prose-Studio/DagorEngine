# Google Breakpad's crash handling client: minidump writing and the exception handler
set(deps 3rdPartyLibs.arc.zlib-ng)
if(WIN32)
  list(APPEND defines UNICODE)
  list(APPEND deps 3rdPartyLibs.breakpad.common.windows)
endif()
if(LINUX)
  list(APPEND deps 3rdPartyLibs.breakpad.common 3rdPartyLibs.breakpad.common.linux)
endif()
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND deps 3rdPartyLibs.breakpad.common 3rdPartyLibs.breakpad.common.mac)
  list(APPEND libs System::pthread)
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND options -Wno-stack-protector)
endif()

dagor_add_target(NAME 3rdPartyLibs.breakpad STATIC LAX
  FILES_CMAKE breakpad_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/breakpad ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zlib-ng
    ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/engine/kernel
  COMPILE_DEFINITIONS PRIVATE ${defines}
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES
    PUBLIC ${libs}
    PRIVATE ${deps}
)
