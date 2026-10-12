set(includes ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources stub.cpp)

dagor_add_library(gameLibs.breakpad.stub ${sources})
target_include_directories(gameLibs.breakpad.stub PRIVATE ${includes})
