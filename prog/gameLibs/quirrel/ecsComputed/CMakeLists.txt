set(includes
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/gameLibs
)
set(sources ecsComputed.cpp)

dagor_add_library(gameLibs.quirrel.ecsComputed ${sources})
target_include_directories(gameLibs.quirrel.ecsComputed PRIVATE ${includes})
target_link_libraries(gameLibs.quirrel.ecsComputed PRIVATE Dagor::Quirrel)
