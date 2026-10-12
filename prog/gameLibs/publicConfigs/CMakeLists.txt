set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources publicConfigs.cpp)

dagor_add_library(gameLibs.publicConfigs LAX ${sources})
target_include_directories(gameLibs.publicConfigs PRIVATE ${includes})
