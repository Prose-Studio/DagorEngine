# Decoding of the SPIR-V shader metadata: chunked containers and SMOL-V decompression
dagor_add_target(NAME engine.drv.shadersMetaData.spirv STATIC LAX
  FILES_CMAKE spirv_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/include ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/smol-v/source
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.vulkan.smol-v
)
