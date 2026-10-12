set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources waterRipples.cpp dropSplashes.cpp)

dagor_add_library(gameLibs.render.waterRipples ${sources})
target_include_directories(gameLibs.render.waterRipples PRIVATE ${includes})
