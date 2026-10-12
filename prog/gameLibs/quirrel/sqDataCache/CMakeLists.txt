set(includes
  ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/engine/sharedInclude
)
set(deps gameLibs.datacache gameLibs.folders)
set(sources datacache.cpp)

dagor_add_library(gameLibs.quirrel.sqDataCache ${sources})
target_include_directories(gameLibs.quirrel.sqDataCache PRIVATE ${includes})
target_link_libraries(gameLibs.quirrel.sqDataCache PRIVATE Dagor::Quirrel ${deps})
