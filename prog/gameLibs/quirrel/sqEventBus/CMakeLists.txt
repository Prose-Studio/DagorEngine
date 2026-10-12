# Quirrel event bus: events between VMs and native code, the eventbus module
set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
)
set(deps gameLibs.quirrel.sqCrossCall)
set(sources sqEventBus.cpp bind.cpp)

dagor_add_library(gameLibs.quirrel.sqEventBus ${sources})
target_include_directories(gameLibs.quirrel.sqEventBus PRIVATE ${includes})
target_link_libraries(gameLibs.quirrel.sqEventBus PRIVATE Dagor::Quirrel ${deps})
