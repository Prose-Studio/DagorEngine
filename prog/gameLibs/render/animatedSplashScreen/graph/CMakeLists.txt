set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources splashGraph.cpp)
set(deps gameLibs.render)

dagor_add_library(gameLibs.render.animatedSplashScreen.graph ${sources})
target_include_directories(gameLibs.render.animatedSplashScreen.graph PRIVATE ${includes})
target_link_libraries(gameLibs.render.animatedSplashScreen.graph PRIVATE ${deps})
