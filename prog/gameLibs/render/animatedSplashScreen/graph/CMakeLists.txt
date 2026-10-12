dagor_add_target(NAME gameLibs.render.animatedSplashScreen.graph STATIC
  FILES_CMAKE graph_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR}
  BUILD_DEPENDENCIES PRIVATE gameLibs.render
)
