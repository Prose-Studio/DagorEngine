set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
)
set(sources sqConsole.cpp)

dagor_add_library(gameLibs.quirrel.sqConsole ${sources})
target_include_directories(gameLibs.quirrel.sqConsole PRIVATE ${includes})
target_link_libraries(gameLibs.quirrel.sqConsole PRIVATE Dagor::Quirrel)
