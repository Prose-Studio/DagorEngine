set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
)
set(deps gameLibs.quirrel.sqEventBus 1stPartyLibs.jsoncpp)
set(sources lastInputMonitor.cpp)

dagor_add_library(gameLibs.quirrel.lastInputMonitor ${sources})
target_include_directories(gameLibs.quirrel.lastInputMonitor PRIVATE ${includes})
target_link_libraries(gameLibs.quirrel.lastInputMonitor PRIVATE Dagor::Quirrel ${deps})
