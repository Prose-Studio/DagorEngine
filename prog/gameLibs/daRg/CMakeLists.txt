# the Quirrel debugger of the games' Dev and Dbg builds on the desktop
set(defines)
if(DAGOR_VARIANT STREQUAL "game" AND CMAKE_SYSTEM_NAME MATCHES "^(Darwin|Linux|Windows)$")
  set(defines "$<$<CONFIG:Dev,Dbg>:DARG_WITH_SQDEBUGGER>")
endif()

dagor_add_target(NAME gameLibs.daRg STATIC
  FILES_CMAKE daRg_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/1stPartyLibs/quirrel ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
    ${DAGOR_PROG_DIR}/gameLibs/daRg ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PRIVATE
    Dagor::Quirrel 3rdPartyLibs.eastl 1stPartyLibs.daScript gameLibs.quirrel.frp gameLibs.frameTimeMetrics
    gameLibs.forceFeedback gameLibs.gesture engine.videoPlayer gameLibs.dasModules.common
    3rdPartyLibs.codecs.libogg-1.1.3 3rdPartyLibs.codecs.libtheora-1.0
)
