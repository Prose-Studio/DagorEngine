set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include)
file(GLOB AllSources RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp")
set(sources ${AllSources})
set(deps 1stPartyLibs.daScript)

dagor_add_library(gameLibs.dasModules.perFrameStat ${sources})
target_include_directories(gameLibs.dasModules.perFrameStat PRIVATE ${includes})
target_link_libraries(gameLibs.dasModules.perFrameStat PRIVATE ${deps})
