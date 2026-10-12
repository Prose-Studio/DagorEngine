set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel)
set(sources sqPerFrameStat.cpp)
set(deps gameLibs.perFrameStat)

dagor_add_library(gameLibs.quirrel.sqPerFrameStat ${sources})
target_include_directories(gameLibs.quirrel.sqPerFrameStat PRIVATE ${includes})
target_link_libraries(gameLibs.quirrel.sqPerFrameStat PRIVATE Dagor::Quirrel ${deps})
