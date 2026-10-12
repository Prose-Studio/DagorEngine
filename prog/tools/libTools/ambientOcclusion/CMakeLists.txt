# Ambient occlusion baking for tools: per-vertex PRT (spherical harmonics) by rays against collision occluders
set(includes ${DAGOR_PROG_DIR}/tools/sharedInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources ambientOcclusion.cpp)

dagor_add_library(tools.libTools.ambientOcclusion LAX ${sources})
target_include_directories(tools.libTools.ambientOcclusion PRIVATE ${includes})
