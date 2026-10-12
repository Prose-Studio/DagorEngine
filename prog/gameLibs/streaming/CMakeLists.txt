set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources streaming.cpp)

dagor_add_library(gameLibs.streaming ${sources})
target_include_directories(gameLibs.streaming PRIVATE ${includes})
