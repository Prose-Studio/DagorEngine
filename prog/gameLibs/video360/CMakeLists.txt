set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources video360.cpp)

dagor_add_library(gameLibs.video360 ${sources})
target_include_directories(gameLibs.video360 PRIVATE ${includes})
