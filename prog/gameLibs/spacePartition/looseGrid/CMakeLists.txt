set(sources looseGrid.cpp)
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)

dagor_add_library(gameLibs.spacePartition.looseGrid LAX ${sources})
target_include_directories(gameLibs.spacePartition.looseGrid PRIVATE ${includes})
