set(includes
  ${DAGOR_PROG_DIR}/engine
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${CMAKE_CURRENT_SOURCE_DIR}
)
set(sources shaderCacheWarmup.cpp startup.cpp)

dagor_add_library(gameLibs.render.shaderCacheWarmup LAX ${sources})
target_include_directories(gameLibs.render.shaderCacheWarmup PRIVATE ${includes})
