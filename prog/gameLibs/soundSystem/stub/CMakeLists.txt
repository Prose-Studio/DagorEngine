set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources soundSystemStub.cpp debugStub.cpp)

dagor_add_library(gameLibs.soundSystem.stub LAX ${sources})
target_include_directories(gameLibs.soundSystem.stub PRIVATE ${includes})
