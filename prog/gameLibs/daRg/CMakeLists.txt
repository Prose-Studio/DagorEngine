# the Quirrel debugger of the games' Dev and Dbg builds on the desktop (prog/daNetGame/setup.jam)
add_subdirectory(browser)
add_subdirectory(stub)

set(defines)
if(DAGOR_VARIANT STREQUAL "game" AND CMAKE_SYSTEM_NAME MATCHES "^(Darwin|Linux|Windows)$")
  set(defines "$<$<CONFIG:Dev,Dbg>:DARG_WITH_SQDEBUGGER>")
endif()
set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/1stPartyLibs/quirrel
  ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  ${DAGOR_PROG_DIR}/gameLibs/daRg
  ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
)
set(AllSrcFolder . behaviors)
dagor_glob_sources(sources DIRS ${AllSrcFolder} GLOB *.cpp)
list(APPEND deps 3rdPartyLibs.eastl 1stPartyLibs.daScript gameLibs.quirrel.frp gameLibs.frameTimeMetrics
  gameLibs.forceFeedback gameLibs.gesture engine.videoPlayer gameLibs.dasModules.common 3rdPartyLibs.codecs.libogg-1.1.3
  3rdPartyLibs.codecs.libtheora-1.0)

dagor_add_library(gameLibs.daRg ${sources})
target_include_directories(gameLibs.daRg PRIVATE ${includes})
target_compile_definitions(gameLibs.daRg PRIVATE ${defines})
target_link_libraries(gameLibs.daRg PRIVATE Dagor::Quirrel ${deps})
