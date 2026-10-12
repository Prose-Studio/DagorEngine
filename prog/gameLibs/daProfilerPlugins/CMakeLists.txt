set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources daProfilerVSync.cpp)
list(APPEND deps engine.perfMon)

dagor_add_library(gameLibs.daProfilerPlugins ${sources})
target_include_directories(gameLibs.daProfilerPlugins PRIVATE ${includes})
target_link_libraries(gameLibs.daProfilerPlugins PRIVATE ${deps})
