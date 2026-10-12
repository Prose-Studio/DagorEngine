# Animation state graph (ASG) data for tools: states, nodes, the anim tree, conditions, loading and export
dagor_add_target(NAME tools.libTools.pageAsg STATIC LAX
  FILES_CMAKE pageAsg_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sharedInclude
)
