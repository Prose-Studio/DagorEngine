# The Vulkan back end of the shader compilers: HLSL to SPIR-V through DXC, optimized with spirv-tools and packed with
# smol-v
find_package(DXC REQUIRED)
set(libs)
if(WIN32)
  set(libs System::d3dcompiler)
endif()
dagor_add_target(NAME tools.ShaderCompiler2.hlsl2spirv STATIC LAX
  FILES_CMAKE hlsl2spirv_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/include ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/smol-v/source
    ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/spirv-tools/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  COMPILE_DEFINITIONS PRIVATE
    _CROSS_TARGET_SPIRV BINDUMP_TARGET_BE=0 _CRT_SECURE_NO_DEPRECATE _HAS_EXCEPTIONS=0 _SECURE_SCL=0 EXCLUDE_PSTDINT
  BUILD_DEPENDENCIES
    PUBLIC ${libs}
    PRIVATE
      3rdPartyLibs.hash 3rdPartyLibs.vulkan.smol-v 3rdPartyLibs.vulkan.spirv-tools 3rdPartyLibs.eastl gameLibs.spirv
      DXC::DXC
)
