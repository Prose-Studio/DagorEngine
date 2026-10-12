set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources consoleKeyBindingsStub.cpp)

dagor_add_library(gameLibs.consoleKeyBindings.consoleKeyBindingsStub ${sources})
target_include_directories(gameLibs.consoleKeyBindings.consoleKeyBindingsStub PRIVATE ${includes})
