add_subdirectory(stub)

set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources cables.cpp)
list(APPEND deps engine.lib3d gameLibs.render)

dagor_add_library(gameLibs.render.cables ${sources})
target_include_directories(gameLibs.render.cables PRIVATE ${includes})
target_link_libraries(gameLibs.render.cables PRIVATE ${deps})
