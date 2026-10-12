set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources animCharTexReplace.cpp)

dagor_add_library(gameLibs.render.animCharTexReplace ${sources})
target_include_directories(gameLibs.render.animCharTexReplace PRIVATE ${includes})
