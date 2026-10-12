set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/engine/sharedInclude
)
set(sources sqStatsd.cpp)

dagor_add_library(gameLibs.quirrel.sqStatsd ${sources})
target_include_directories(gameLibs.quirrel.sqStatsd PRIVATE ${includes})
target_link_libraries(gameLibs.quirrel.sqStatsd PRIVATE Dagor::Quirrel)
