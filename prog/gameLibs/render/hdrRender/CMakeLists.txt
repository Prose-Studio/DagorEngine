add_subdirectory(stub)

set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources hdrRender.cpp hdrDecoder.cpp)

dagor_add_library(gameLibs.render.hdrRender ${sources})
target_include_directories(gameLibs.render.hdrRender PRIVATE ${includes})
