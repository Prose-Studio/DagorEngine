set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources antialiasingStub.cpp)

dagor_add_library(gameLibs.render.antialiasing.stub LAX ${sources})
target_include_directories(gameLibs.render.antialiasing.stub PRIVATE ${includes})
