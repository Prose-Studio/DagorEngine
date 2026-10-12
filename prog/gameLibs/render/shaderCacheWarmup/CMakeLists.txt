dagor_add_target(NAME gameLibs.render.shaderCacheWarmup STATIC LAX
  FILES_CMAKE shaderCacheWarmup_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/engine ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    ${CMAKE_CURRENT_SOURCE_DIR}
)
