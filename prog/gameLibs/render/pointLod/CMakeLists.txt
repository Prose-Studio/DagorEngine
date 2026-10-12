# Point cloud LOD: ranges that keep a point density without holes, density scaling by distance
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources range.cpp)

dagor_add_library(gameLibs.render.pointLod ${sources})
target_include_directories(gameLibs.render.pointLod PRIVATE ${includes})
