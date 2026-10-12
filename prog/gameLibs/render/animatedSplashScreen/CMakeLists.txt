dagor_add_target(NAME gameLibs.render.animatedSplashScreen STATIC
  FILES_CMAKE animatedSplashScreen_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/render/animatedSplashScreen/public_api
    ${DAGOR_PROG_DIR}/gameLibs/render/animatedSplashScreen/graph
  BUILD_DEPENDENCIES PRIVATE
    gameLibs.render gameLibs.render.hdrRender gameLibs.render.shaderCacheWarmup gameLibs.render.antialiasing
    gameLibs.render.animatedSplashScreen.graph
)
