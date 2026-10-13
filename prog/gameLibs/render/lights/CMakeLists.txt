# Dynamic lights: omni and spot light managers, clustered and tiled light culling, light shadows
dagor_add_target(NAME gameLibs.render.lights STATIC LAX
  FILES_CMAKE lights_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR} ${DAGOR_PROG_DIR}/gameLibs/render/shaders
    ${DAGOR_PROG_DIR}/3rdPartyLibs/binPack2D/include
)
