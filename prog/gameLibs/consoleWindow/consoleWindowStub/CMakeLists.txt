set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources consoleWindowStub.cpp)

dagor_add_library(gameLibs.consoleWindow.consoleWindowStub ${sources})
target_include_directories(gameLibs.consoleWindow.consoleWindowStub PRIVATE ${includes})
