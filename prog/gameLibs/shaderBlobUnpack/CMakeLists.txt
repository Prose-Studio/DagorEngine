# Shader blob unpacking for tools: detects the API (DX11, DXIL, SPIR-V) and extracts each stage's bytecode
dagor_add_target(NAME gameLibs.shaderBlobUnpack STATIC LAX
  FILES_CMAKE shaderBlobUnpack_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/include
  BUILD_DEPENDENCIES PRIVATE
    engine.drv.shadersMetaData engine.drv.shadersMetaData.dx11 engine.drv.shadersMetaData.dxil
    engine.drv.shadersMetaData.spirv
)
