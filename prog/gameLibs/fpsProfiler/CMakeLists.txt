set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources perfRating.cpp)

dagor_add_library(gameLibs.fpsProfiler ${sources})
target_include_directories(gameLibs.fpsProfiler PRIVATE ${includes})
