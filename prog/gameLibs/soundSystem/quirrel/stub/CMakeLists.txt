set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources soundSystemSqStub.cpp)

dagor_add_library(gameLibs.soundSystem.quirrel.stub ${sources})
target_include_directories(gameLibs.soundSystem.quirrel.stub PRIVATE ${includes})
target_link_libraries(gameLibs.soundSystem.quirrel.stub PRIVATE Dagor::Quirrel)
