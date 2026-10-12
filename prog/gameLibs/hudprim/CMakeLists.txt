set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources hudPrimitives.cpp)

dagor_add_library(gameLibs.hudprim LAX ${sources})
target_include_directories(gameLibs.hudprim PRIVATE ${includes})
