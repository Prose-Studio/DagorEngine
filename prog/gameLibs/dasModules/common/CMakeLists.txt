# daScript modules of the engine: files, DataBlock, console, math, debug drawing
set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5
)
file(GLOB AllSources RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp")
set(sources ${AllSources})
set(SourceDAS dagorFiles.das dagorDataBlock.das dagorConsole.das dagorMath.das dagorDebug3d.das)
list(APPEND stringify ${SourceDAS})
if(WIN32)
  list(APPEND options /wd4548)
endif()
set(deps 1stPartyLibs.daScript 3rdPartyLibs.arc.zstd-1.4.5)

dagor_add_library(gameLibs.dasModules.common ${sources})
target_include_directories(gameLibs.dasModules.common PRIVATE ${includes})
target_compile_options(gameLibs.dasModules.common PRIVATE ${options})
target_link_libraries(gameLibs.dasModules.common PRIVATE ${deps})
dagor_target_stringify(gameLibs.dasModules.common ${stringify})
