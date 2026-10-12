set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources gameTimers.cpp)

dagor_add_library(gameLibs.daGame.timers ${sources})
target_include_directories(gameLibs.daGame.timers PRIVATE ${includes})
