set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/dagorInclude)
set(sources psoCacheLoader.cpp)
list(APPEND deps engine.lib3d)

dagor_add_library(gameLibs.render.psoCacheLoader ${sources})
target_include_directories(gameLibs.render.psoCacheLoader PRIVATE ${includes})
target_link_libraries(gameLibs.render.psoCacheLoader PRIVATE ${deps})
