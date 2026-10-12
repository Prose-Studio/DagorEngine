set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources heatHazeRenderer.cpp)

dagor_add_library(gameLibs.render.heatHaze ${sources})
target_include_directories(gameLibs.render.heatHaze PRIVATE ${includes})
