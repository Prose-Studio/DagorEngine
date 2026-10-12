# Texture compression: BC1/BC3/BC5 on the GPU and DXT on the CPU
dagor_add_target(NAME gameLibs.render.texcompressors STATIC
  FILES_CMAKE texcompressors_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
