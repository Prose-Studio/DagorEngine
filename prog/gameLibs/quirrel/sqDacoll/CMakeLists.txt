set(includes
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
)
set(sources sqDacoll.cpp)
list(APPEND deps Dagor::Phys)

dagor_add_library(gameLibs.quirrel.sqDacoll ${sources})
target_include_directories(gameLibs.quirrel.sqDacoll PRIVATE ${includes})
target_link_libraries(gameLibs.quirrel.sqDacoll PRIVATE Dagor::Quirrel ${deps})
