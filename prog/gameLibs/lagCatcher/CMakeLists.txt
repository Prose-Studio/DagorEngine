set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources lagCatcher.cpp)
if(LINUX)
  list(APPEND sources btCollector.cpp utils.cpp)
endif()

dagor_add_library(gameLibs.lagCatcher ${sources})
target_include_directories(gameLibs.lagCatcher PRIVATE ${includes})
