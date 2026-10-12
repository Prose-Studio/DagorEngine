# Shader blob unpacking for tools: detects the API (DX11, DXIL, SPIR-V) and extracts each stage's bytecode
set(sources blobUnpack.cpp)
list(APPEND includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/include)
list(APPEND deps engine.drv.shadersMetaData engine.drv.shadersMetaData.dx11 engine.drv.shadersMetaData.dxil
  engine.drv.shadersMetaData.spirv)

dagor_add_library(gameLibs.shaderBlobUnpack LAX ${sources})
target_include_directories(gameLibs.shaderBlobUnpack PRIVATE ${includes})
target_link_libraries(gameLibs.shaderBlobUnpack PRIVATE ${deps})
