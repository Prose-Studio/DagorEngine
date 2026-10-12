set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
if(DAGOR_GAME_BVH)
  set(sources rtao.cpp)
else()
  set(sources rtao_stub.cpp)
endif()

dagor_add_library(gameLibs.render.rtao ${sources})
target_include_directories(gameLibs.render.rtao PRIVATE ${includes})
