set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources objectMotionBlur.cpp)

dagor_add_library(gameLibs.render.objectMotionBlur ${sources})
target_include_directories(gameLibs.render.objectMotionBlur PRIVATE ${includes})
