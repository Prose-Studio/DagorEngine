set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources visconstub.cpp)

dagor_add_library(gameLibs.visualConsole.visconstub ${sources})
target_include_directories(gameLibs.visualConsole.visconstub PRIVATE ${includes})
