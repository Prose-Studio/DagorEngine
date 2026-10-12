set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources statsd.cpp log.cpp)
list(APPEND deps gameLibs.asyncResolveAddr)

dagor_add_library(gameLibs.statsd ${sources})
target_include_directories(gameLibs.statsd PRIVATE ${includes})
target_link_libraries(gameLibs.statsd PRIVATE ${deps})
