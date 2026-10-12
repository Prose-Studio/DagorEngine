set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
dagor_glob_sources(sources DIRS . GLOB *.cpp)

dagor_add_library(gameLibs.daFracture.core ${sources})
target_include_directories(gameLibs.daFracture.core PRIVATE ${includes})
