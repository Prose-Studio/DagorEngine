set(includes ${DAGOR_PROG_DIR}/3rdPartyLibs/codecs/include)
if(CMAKE_SYSTEM_NAME MATCHES "^(Android|Darwin|Linux|Windows|iOS|tvOS)$")
  list(APPEND includes
    ${DAGOR_PROG_DIR}/3rdPartyLibs/codecs/dav1d/include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/codecs/dav1d/include/common
    ${DAGOR_PROG_DIR}/3rdPartyLibs/codecs/dav1d/include/dav1d
    ${DAGOR_PROG_DIR}/3rdPartyLibs/codecs/dav1d/tools
  )
  list(APPEND deps 3rdPartyLibs.codecs.dav1d)
  if(DAGOR_ARCH STREQUAL "x86_64" AND WIN32)
    list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/codecs/dav1d/generated/win64)
  endif()
  if(WIN32 AND DAGOR_ARCH STREQUAL "arm64")
    list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/codecs/dav1d/generated/windows_arm64)
  endif()
  if(LINUX)
    list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/codecs/dav1d/generated/linux)
  endif()
  if(IOS)
    list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/codecs/dav1d/generated/macosx_arm64)
  endif()
  if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
    if(DAGOR_ARCH STREQUAL "arm64")
      list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/codecs/dav1d/generated/macosx_arm64)
    else()
      list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/codecs/dav1d/generated/macosx_x86_64)
    endif()
  endif()
  if(ANDROID)
    if(DAGOR_ARCH STREQUAL "arm64")
      list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/codecs/dav1d/generated/android/aarch64)
    else()
      list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/codecs/dav1d/generated/android/arm)
    endif()
  endif()
  list(APPEND defines BITDEPTH=8 SUPPORT_AV1)
endif()

dagor_add_target(NAME engine.videoPlayer STATIC
  FILES_CMAKE videoPlayer_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
