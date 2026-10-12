set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources lruCollision.cpp)

dagor_add_library(gameLibs.render.lruCollision ${sources})
target_include_directories(gameLibs.render.lruCollision PRIVATE ${includes})
