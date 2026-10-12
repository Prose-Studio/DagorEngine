set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources dof_ps.cpp)

dagor_add_library(gameLibs.render.dof ${sources})
target_include_directories(gameLibs.render.dof PRIVATE ${includes})
