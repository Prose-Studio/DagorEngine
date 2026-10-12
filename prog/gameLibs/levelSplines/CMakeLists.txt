set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources levelSplines.cpp splineRegions.cpp splineRoads.cpp splineDebugDraw.cpp)

dagor_add_library(gameLibs.levelSplines LAX ${sources})
target_include_directories(gameLibs.levelSplines PRIVATE ${includes})
