set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
)
set(sources clientLog.cpp)

dagor_add_library(gameLibs.quirrel.clientLog ${sources})
target_include_directories(gameLibs.quirrel.clientLog PRIVATE ${includes})
target_link_libraries(gameLibs.quirrel.clientLog PRIVATE Dagor::Quirrel)
