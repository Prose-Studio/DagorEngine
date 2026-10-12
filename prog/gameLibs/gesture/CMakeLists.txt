set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources gestureDetector.cpp)

dagor_add_library(gameLibs.gesture ${sources})
target_include_directories(gameLibs.gesture PRIVATE ${includes})
