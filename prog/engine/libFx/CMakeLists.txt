# Common effects support: fx texture prefetching for texture streaming and the leaves wind effect
dagor_add_target(NAME engine.libFx STATIC LAX
  FILES_CMAKE libFx_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
)
