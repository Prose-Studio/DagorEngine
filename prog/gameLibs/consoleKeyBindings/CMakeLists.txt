add_subdirectory(consoleKeyBindingsStub)

set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources consoleKeyBindings.cpp)

dagor_add_library(gameLibs.consoleKeyBindings ${sources})
target_include_directories(gameLibs.consoleKeyBindings PRIVATE ${includes})
