set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources hdrRender.cpp)

dagor_add_library(gameLibs.render.hdrRender.stub ${sources})
target_include_directories(gameLibs.render.hdrRender.stub PRIVATE ${includes})
