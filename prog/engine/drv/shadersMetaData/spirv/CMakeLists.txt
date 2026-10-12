# Decoding of the SPIR-V shader metadata: chunked containers and SMOL-V decompression
set(sources unpack.cpp)
list(APPEND includes
  ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/smol-v/source
)
list(APPEND deps 3rdPartyLibs.vulkan.smol-v)

dagor_add_library(engine.drv.shadersMetaData.spirv LAX ${sources})
target_include_directories(engine.drv.shadersMetaData.spirv PRIVATE ${includes})
target_link_libraries(engine.drv.shadersMetaData.spirv PRIVATE ${deps})
