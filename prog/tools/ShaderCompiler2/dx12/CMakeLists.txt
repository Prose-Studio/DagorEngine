# The DX12 back end of the shader compilers: HLSL to DXIL through DXC (with FXC still the preprocessor, as DXC follows
# the proper C preprocessor rules and not MS's ones)
find_package(DXC REQUIRED)
dagor_add_library(tools.ShaderCompiler2.dx12 LAX asmShaderDXIL.cpp)
target_include_directories(tools.ShaderCompiler2.dx12 PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/3rdPartyLibs/memAllocators/mimalloc/include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/memAllocators/mimalloc/mimalloc/include)
target_compile_definitions(tools.ShaderCompiler2.dx12 PRIVATE _CROSS_TARGET_DX12 _CROSS_TARGET_DX12_DXIL
  BINDUMP_TARGET_BE=0 _CRT_SECURE_NO_DEPRECATE _HAS_EXCEPTIONS=0 _SECURE_SCL=0 EXCLUDE_PSTDINT)
target_link_libraries(tools.ShaderCompiler2.dx12 PRIVATE 3rdPartyLibs.hash 3rdPartyLibs.memAllocators.mimalloc.nodebug
  gameLibs.dxil DXC::DXC)
target_link_libraries(tools.ShaderCompiler2.dx12 PUBLIC System::d3dcompiler)
