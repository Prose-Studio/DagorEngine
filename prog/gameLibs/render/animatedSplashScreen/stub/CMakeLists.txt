set(includes ${DAGOR_PROG_DIR}/gameLibs/render/animatedSplashScreen/public_api)
set(sources animatedSplashScreenStub.cpp)

dagor_add_library(gameLibs.render.animatedSplashScreen.stub ${sources})
target_include_directories(gameLibs.render.animatedSplashScreen.stub PRIVATE ${includes})
