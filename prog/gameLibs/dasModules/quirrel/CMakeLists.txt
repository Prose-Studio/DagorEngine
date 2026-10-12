set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/modules/dasQuirrel/src
)
file(GLOB AllSources RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp")
set(sources ${AllSources})
if(WIN32)
  list(APPEND options /wd4548)
endif()
set(deps 1stPartyLibs.daScript gameLibs.ecs.scripts.das 1stPartyLibs.daScript.modules.dasQuirrel)

dagor_add_library(gameLibs.dasModules.quirrel ${sources})
target_include_directories(gameLibs.dasModules.quirrel PRIVATE ${includes})
target_compile_options(gameLibs.dasModules.quirrel PRIVATE ${options})
target_link_libraries(gameLibs.dasModules.quirrel PRIVATE Dagor::Quirrel ${deps})
