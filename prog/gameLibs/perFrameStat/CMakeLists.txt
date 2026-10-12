set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources perFrameStat.cpp)
list(APPEND deps engine.workCycle gameLibs.render)

dagor_add_library(gameLibs.perFrameStat ${sources})
target_include_directories(gameLibs.perFrameStat PRIVATE ${includes})
target_link_libraries(gameLibs.perFrameStat PRIVATE ${deps})
