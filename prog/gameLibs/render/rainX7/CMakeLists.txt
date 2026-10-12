set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources rainX7.cpp)

dagor_add_library(gameLibs.render.rainX7 ${sources})
target_include_directories(gameLibs.render.rainX7 PRIVATE ${includes})
