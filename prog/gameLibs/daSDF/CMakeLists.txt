set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR} shaders)
set(sources worldSDF.cpp)
list(APPEND deps engine.lib3d)

dagor_add_library(gameLibs.daSDF ${sources})
target_include_directories(gameLibs.daSDF PRIVATE ${includes})
target_link_libraries(gameLibs.daSDF PRIVATE ${deps})
