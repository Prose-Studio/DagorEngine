set(sources aggregator.cpp)
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)

dagor_add_library(gameLibs.frameTimeMetrics LAX ${sources})
target_include_directories(gameLibs.frameTimeMetrics PRIVATE ${includes})
