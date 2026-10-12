set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources spatialHashGrid.cpp)
list(APPEND deps gameLibs.gameMath)

dagor_add_library(gameLibs.grid ${sources})
target_include_directories(gameLibs.grid PRIVATE ${includes})
target_link_libraries(gameLibs.grid PRIVATE ${deps})
