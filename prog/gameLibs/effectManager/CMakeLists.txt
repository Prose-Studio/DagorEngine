set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/commonFx/commonFxGame)
if(DAGOR_GAME_RENDERER)
  list(APPEND sources effectManager.cpp)
else()
  list(APPEND sources stub/effectManagerStub.cpp)
endif()

dagor_add_library(gameLibs.effectManager ${sources})
target_include_directories(gameLibs.effectManager PRIVATE ${includes})
