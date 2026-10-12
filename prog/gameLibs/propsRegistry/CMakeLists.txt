set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources propsRegistry.cpp)

dagor_add_library(gameLibs.propsRegistry LAX ${sources})
target_include_directories(gameLibs.propsRegistry PRIVATE ${includes})
