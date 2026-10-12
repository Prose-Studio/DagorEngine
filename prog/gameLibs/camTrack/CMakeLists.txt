set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources camTrack.cpp)

dagor_add_library(gameLibs.camTrack ${sources})
target_include_directories(gameLibs.camTrack PRIVATE ${includes})
