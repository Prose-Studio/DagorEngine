# Tools math: k-DOP bounding volumes
dagor_add_target(NAME tools.libTools.math STATIC LAX
  FILES_CMAKE math_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sharedInclude
)
