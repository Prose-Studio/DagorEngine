set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources renderSq.cpp)
set(deps gameLibs.quirrel.bindQuirrelEx)

dagor_add_library(gameLibs.render.quirrel ${sources})
target_include_directories(gameLibs.render.quirrel PRIVATE ${includes})
target_link_libraries(gameLibs.render.quirrel PRIVATE Dagor::Quirrel ${deps})
