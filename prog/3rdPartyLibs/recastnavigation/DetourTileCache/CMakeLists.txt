if(LINUX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  if(WIN32)
    list(APPEND options -fp:fast)
    if(NOT DAGOR_ARCH STREQUAL "arm64")
      list(APPEND options /clang:-fno-unsafe-math-optimizations)
    endif()
  else()
    list(APPEND options -ffast-math)
    if(NOT IOS AND NOT DAGOR_ARCH STREQUAL "e2k")
      list(APPEND options -fno-unsafe-math-optimizations)
    endif()
  endif()
endif()

dagor_add_target(NAME 3rdPartyLibs.recastnavigation.DetourTileCache STATIC LAX
  FILES_CMAKE DetourTileCache_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/recastnavigation/DetourTileCache/Include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/recastnavigation/Detour/Include
  COMPILE_DEFINITIONS PRIVATE _RELEASE
  COMPILE_OPTIONS PRIVATE ${options}
)
