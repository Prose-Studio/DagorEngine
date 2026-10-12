set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources genericLUT.cpp commonLUT.cpp colorGradingLUT.cpp fullColorGradingLUT.cpp dynamicLUT.cpp)

dagor_add_library(gameLibs.render.genericLUT ${sources})
target_include_directories(gameLibs.render.genericLUT PRIVATE ${includes})
