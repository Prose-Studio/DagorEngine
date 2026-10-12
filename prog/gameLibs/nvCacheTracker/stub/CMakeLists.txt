set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources nvCacheTracker.cpp)

dagor_add_library(gameLibs.nvCacheTracker.stub ${sources})
target_include_directories(gameLibs.nvCacheTracker.stub PRIVATE ${includes})
