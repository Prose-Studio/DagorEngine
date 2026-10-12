set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  ${DAGOR_PROG_DIR}/1stPartyLibs/rapidJsonUtils/include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
)
file(GLOB AllSources RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp")
set(sources ${AllSources})
set(SourceDAS animchar.das zones.das dagorFindFiles.das grid.das)
list(APPEND stringify ${SourceDAS})
if(WIN32)
  list(APPEND options /wd4548)
  list(APPEND defines "$<$<NOT:$<CONFIG:Rel>>:ANIM_PBC_HOT_RELOAD_ENABLED>") # jam had it on Windows only
endif()
set(deps 1stPartyLibs.daScript gameLibs.gameMath)
list(APPEND deps Dagor::Phys)

dagor_add_library(gameLibs.dasModules.generic ${sources})
target_include_directories(gameLibs.dasModules.generic PRIVATE ${includes})
target_compile_definitions(gameLibs.dasModules.generic PRIVATE ${defines})
target_compile_options(gameLibs.dasModules.generic PRIVATE ${options})
target_link_libraries(gameLibs.dasModules.generic PRIVATE ${deps})
dagor_target_stringify(gameLibs.dasModules.generic ${stringify})
