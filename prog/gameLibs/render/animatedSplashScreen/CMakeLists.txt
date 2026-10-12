add_subdirectory(graph)
add_subdirectory(stub)

set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/render/animatedSplashScreen/public_api
  ${DAGOR_PROG_DIR}/gameLibs/render/animatedSplashScreen/graph
)
set(sources animatedSplashScreen.cpp)
set(deps gameLibs.render gameLibs.render.hdrRender gameLibs.render.shaderCacheWarmup gameLibs.render.antialiasing
  gameLibs.render.animatedSplashScreen.graph)

dagor_add_library(gameLibs.render.animatedSplashScreen ${sources})
target_include_directories(gameLibs.render.animatedSplashScreen PRIVATE ${includes})
target_link_libraries(gameLibs.render.animatedSplashScreen PRIVATE ${deps})
