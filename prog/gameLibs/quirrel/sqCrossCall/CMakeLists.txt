# Copying Quirrel values and calls between two Quirrel VMs
set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/engine/sharedInclude
)
set(sources sqCrossCall.cpp)

dagor_add_library(gameLibs.quirrel.sqCrossCall ${sources})
target_include_directories(gameLibs.quirrel.sqCrossCall PRIVATE ${includes})
target_link_libraries(gameLibs.quirrel.sqCrossCall PRIVATE Dagor::Quirrel)
