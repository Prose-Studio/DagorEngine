set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/render)
set(sources upscaleSampling.cpp)

dagor_add_library(gameLibs.render.upscale ${sources})
target_include_directories(gameLibs.render.upscale PRIVATE ${includes})
