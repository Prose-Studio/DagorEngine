# DAG file reading and writing: scene import, geometry mesh helpers, node trees, splines, textures, materials
dagor_add_target(NAME tools.libTools.dagFileRW STATIC LAX
  FILES_CMAKE dagFileRW_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sharedInclude ${DAGOR_PROG_DIR}/engine/sharedInclude
)
