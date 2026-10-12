# The DX12 back end of the shader compilers: HLSL to DXIL through DXC (with FXC still the preprocessor, as DXC follows
# the proper C preprocessor rules and not MS's ones)
find_package(DXC REQUIRED)
dagor_add_target(NAME tools.ShaderCompiler2.dx12 STATIC LAX
  FILES_CMAKE dx12_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/memAllocators/mimalloc/include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/memAllocators/mimalloc/mimalloc/include
  COMPILE_DEFINITIONS PRIVATE
    _CROSS_TARGET_DX12 _CROSS_TARGET_DX12_DXIL BINDUMP_TARGET_BE=0 _CRT_SECURE_NO_DEPRECATE _HAS_EXCEPTIONS=0
    _SECURE_SCL=0 EXCLUDE_PSTDINT
  BUILD_DEPENDENCIES
    PUBLIC System::d3dcompiler
    PRIVATE 3rdPartyLibs.hash 3rdPartyLibs.memAllocators.mimalloc.nodebug gameLibs.dxil DXC::DXC
)
