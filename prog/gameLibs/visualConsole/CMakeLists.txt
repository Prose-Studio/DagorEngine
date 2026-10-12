add_subdirectory(visconstub)

set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources visualConsole.cpp)

dagor_add_library(gameLibs.visualConsole ${sources})
target_include_directories(gameLibs.visualConsole PRIVATE ${includes})
