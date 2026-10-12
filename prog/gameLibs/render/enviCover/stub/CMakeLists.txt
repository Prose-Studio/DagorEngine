set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources enviCoverStub.cpp)

dagor_add_library(gameLibs.render.enviCover.stub LAX ${sources})
target_include_directories(gameLibs.render.enviCover.stub PRIVATE ${includes})
