# Point cloud LOD: ranges that keep a point density without holes, density scaling by distance
dagor_add_target(NAME gameLibs.render.pointLod STATIC
  FILES_CMAKE pointLod_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
