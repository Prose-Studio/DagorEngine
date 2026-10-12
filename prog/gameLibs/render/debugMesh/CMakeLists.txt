# Debug mesh coloring modes (the debug gbuffer modes, overdraw) and their console command
dagor_add_target(NAME gameLibs.render.debugMesh STATIC
  FILES_CMAKE debugMesh_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
