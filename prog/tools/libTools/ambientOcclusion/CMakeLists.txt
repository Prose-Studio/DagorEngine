# Ambient occlusion baking for tools: per-vertex PRT (spherical harmonics) by rays against collision occluders
dagor_add_target(NAME tools.libTools.ambientOcclusion STATIC LAX
  FILES_CMAKE ambientOcclusion_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sharedInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
