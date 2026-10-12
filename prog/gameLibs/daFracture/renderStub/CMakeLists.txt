set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources stub.cpp)

dagor_add_library(gameLibs.daFracture.renderStub ${sources})
target_include_directories(gameLibs.daFracture.renderStub PRIVATE ${includes})
