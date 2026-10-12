set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
if(DAGOR_GAME_BVH)
  set(sources ptgi.cpp)
else()
  set(sources ptgi_stub.cpp)
endif()

dagor_add_library(gameLibs.render.ptgi ${sources})
target_include_directories(gameLibs.render.ptgi PRIVATE ${includes})
