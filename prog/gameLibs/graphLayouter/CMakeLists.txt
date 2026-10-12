# Graph layout for node graph visualizations
set(sources defaultGraphLayouter.cpp)
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)

dagor_add_library(gameLibs.graphLayouter ${sources})
target_include_directories(gameLibs.graphLayouter PRIVATE ${includes})
