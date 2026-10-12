set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/engine/dagorInclude
  ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
)
file(GLOB AllSources RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp")
set(sources ${AllSources})
list(APPEND deps gameLibs.quirrel.quirrel_json)

dagor_add_library(gameLibs.ecs.scripts.sq ${sources})
target_include_directories(gameLibs.ecs.scripts.sq PRIVATE ${includes})
target_link_libraries(gameLibs.ecs.scripts.sq PRIVATE Dagor::Quirrel ${deps})
