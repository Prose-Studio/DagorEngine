set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources cablesStub.cpp)

dagor_add_library(gameLibs.render.cables.stub ${sources})
target_include_directories(gameLibs.render.cables.stub PRIVATE ${includes})
