set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources textureUtil.cpp)

dagor_add_library(gameLibs.textureUtil ${sources})
target_include_directories(gameLibs.textureUtil PRIVATE ${includes})
