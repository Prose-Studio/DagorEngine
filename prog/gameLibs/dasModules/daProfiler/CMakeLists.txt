set(includes
  ${DAGOR_PROG_DIR}/engine/dagorInclude
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
)
file(GLOB AllSources RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp")
set(sources ${AllSources})
if(WIN32)
  list(APPEND options /wd4548)
endif()
set(deps 1stPartyLibs.daScript engine.perfMon gameLibs.folders)

dagor_add_library(gameLibs.dasModules.daProfiler ${sources})
target_include_directories(gameLibs.dasModules.daProfiler PRIVATE ${includes})
target_compile_options(gameLibs.dasModules.daProfiler PRIVATE ${options})
target_link_libraries(gameLibs.dasModules.daProfiler PRIVATE ${deps})
