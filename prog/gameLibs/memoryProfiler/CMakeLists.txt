set(sources memstat.cpp)
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)

dagor_add_library(gameLibs.memoryProfiler LAX ${sources})
target_include_directories(gameLibs.memoryProfiler PRIVATE ${includes})
