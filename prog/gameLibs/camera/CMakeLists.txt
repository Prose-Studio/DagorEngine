set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources cameraShaker.cpp valueShaker.cpp)

dagor_add_library(gameLibs.camera ${sources})
target_include_directories(gameLibs.camera PRIVATE ${includes})
