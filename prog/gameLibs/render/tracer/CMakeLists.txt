set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources tracer.cpp)

dagor_add_library(gameLibs.render.tracer ${sources})
target_include_directories(gameLibs.render.tracer PRIVATE ${includes})
