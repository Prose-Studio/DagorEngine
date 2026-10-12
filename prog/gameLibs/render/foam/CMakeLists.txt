set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources foamFx.cpp)

dagor_add_library(gameLibs.render.foam ${sources})
target_include_directories(gameLibs.render.foam PRIVATE ${includes})
