# Texture compression: BC1/BC3/BC5 on the GPU and DXT on the CPU
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources dxtcompress.cpp bcCompressor.cpp)

dagor_add_library(gameLibs.render.texcompressors ${sources})
target_include_directories(gameLibs.render.texcompressors PRIVATE ${includes})
