set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources actionStub.cpp dargSqBindStub.cpp)

dagor_add_library(gameLibs.daInput.stub ${sources})
target_include_directories(gameLibs.daInput.stub PRIVATE ${includes})
