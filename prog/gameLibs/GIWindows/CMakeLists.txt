set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR} shaders)
set(sources giWindows.cpp)
list(APPEND deps engine.lib3d)

dagor_add_library(gameLibs.GIWindows ${sources})
target_include_directories(gameLibs.GIWindows PRIVATE ${includes})
target_link_libraries(gameLibs.GIWindows PRIVATE ${deps})
