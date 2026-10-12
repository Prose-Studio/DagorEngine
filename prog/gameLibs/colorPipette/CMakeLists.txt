set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources colorPipette.cpp)
list(APPEND deps gameLibs.gameMath)

dagor_add_library(gameLibs.colorPipette ${sources})
target_include_directories(gameLibs.colorPipette PRIVATE ${includes})
target_link_libraries(gameLibs.colorPipette PRIVATE ${deps})
