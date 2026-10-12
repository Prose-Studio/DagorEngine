add_subdirectory(consoleWindowStub)

set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources consoleWindow.cpp)

dagor_add_library(gameLibs.consoleWindow ${sources})
target_include_directories(gameLibs.consoleWindow PRIVATE ${includes})
