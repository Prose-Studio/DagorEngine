# Pools of reusable GPU resources and aliasable managed 2D textures
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources aliasableTex.cpp resourcePool.cpp)
list(APPEND deps engine.lib3d)

dagor_add_library(gameLibs.resourcePool ${sources})
target_include_directories(gameLibs.resourcePool PRIVATE ${includes})
target_link_libraries(gameLibs.resourcePool PRIVATE ${deps})
