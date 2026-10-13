set(includes
  ${DAGOR_PROG_DIR}/3rdPartyLibs/crashpad
  ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zlib-ng
  ${DAGOR_PROG_DIR}/3rdPartyLibs/crashpad/third_party/mini_chromium/mini_chromium
)
list(APPEND defines CRASHPAD_ZLIB_SOURCE_EXTERNAL)
if(DAGOR_SANITIZE STREQUAL "address")
  list(APPEND defines ADDRESS_SANITIZER)
endif()
if(WIN32)
  list(APPEND defines UNICODE CRASHPAD_FLOCK_ALWAYS_SUPPORTED)
  list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/crashpad/compat/win)
  if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    list(APPEND options -Wno-format)
  endif()
endif()

dagor_add_target(NAME 3rdPartyLibs.crashpad STATIC LAX
  FILES_CMAKE crashpad_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE ${defines}
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.arc.zlib-ng
)
