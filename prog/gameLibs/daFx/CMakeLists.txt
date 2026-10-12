# daFx: the particle effects runtime (systems, emitters, instances, GPU buffers, culling and rendering)
dagor_add_target(NAME gameLibs.daFx STATIC
  FILES_CMAKE daFx_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
