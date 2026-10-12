set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources cloudsFieldDebug.cpp)
list(APPEND deps gameLibs.render.daFrameGraph)

dagor_add_library(gameLibs.daSkies2.debug ${sources})
target_include_directories(gameLibs.daSkies2.debug PRIVATE ${includes})
target_link_libraries(gameLibs.daSkies2.debug PRIVATE ${deps})
