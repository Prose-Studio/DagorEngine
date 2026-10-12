set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources collisionOccluders_legacy.cpp)

dagor_add_library(gameLibs.collisionOccluders ${sources})
target_include_directories(gameLibs.collisionOccluders PRIVATE ${includes})
