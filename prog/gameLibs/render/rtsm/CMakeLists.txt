set(includes ${DAGOR_PROG_DIR}/gameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
if(DAGOR_GAME_BVH)
  set(sources rtsm.cpp)
else()
  set(sources rtsm_stub.cpp)
endif()

dagor_add_library(gameLibs.render.rtsm ${sources})
target_include_directories(gameLibs.render.rtsm PRIVATE ${includes})
