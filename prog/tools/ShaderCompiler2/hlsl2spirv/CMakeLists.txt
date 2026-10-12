# The Vulkan back end of the shader compilers: HLSL to SPIR-V through DXC, optimized with spirv-tools and packed with
# smol-v
find_package(DXC REQUIRED)
set(libs)
if(WIN32)
  set(libs System::d3dcompiler)
endif()
dagor_add_library(tools.ShaderCompiler2.hlsl2spirv LAX asmShaderSpirV.cpp HLSL2SpirvCommon.cpp)
target_include_directories(tools.ShaderCompiler2.hlsl2spirv PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/smol-v/source ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/spirv-tools/include
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
target_compile_definitions(tools.ShaderCompiler2.hlsl2spirv PRIVATE _CROSS_TARGET_SPIRV BINDUMP_TARGET_BE=0
  _CRT_SECURE_NO_DEPRECATE _HAS_EXCEPTIONS=0 _SECURE_SCL=0 EXCLUDE_PSTDINT)
target_link_libraries(tools.ShaderCompiler2.hlsl2spirv PRIVATE 3rdPartyLibs.hash 3rdPartyLibs.vulkan.smol-v
  3rdPartyLibs.vulkan.spirv-tools 3rdPartyLibs.eastl gameLibs.spirv DXC::DXC)
target_link_libraries(tools.ShaderCompiler2.hlsl2spirv PUBLIC ${libs})
