set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources
  fluidWind.cpp
  ambientWind.cpp
  clusterWind.cpp
  clusterWindCascade.cpp
  clusterWindRenderer.cpp
  fxWindHelper.cpp
)

dagor_add_library(gameLibs.render.wind ${sources})
target_include_directories(gameLibs.render.wind PRIVATE ${includes})
