set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources indoorProbeManager.cpp indoorProbeScenes.cpp)

dagor_add_library(gameLibs.render.indoorProbes ${sources})
target_include_directories(gameLibs.render.indoorProbes PRIVATE ${includes})
