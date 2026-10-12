set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
if(DAGOR_GAME_BVH)
  set(sources rtr.cpp)
else()
  set(sources rtr_stub.cpp)
endif()

dagor_add_library(gameLibs.render.rtr ${sources})
target_include_directories(gameLibs.render.rtr PRIVATE ${includes})
