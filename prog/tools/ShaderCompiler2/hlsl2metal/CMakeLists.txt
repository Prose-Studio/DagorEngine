if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND options -Wno-deprecated-declarations)
endif()

dagor_add_target(NAME tools.ShaderCompiler2.hlsl2metal STATIC LAX
  FILES_CMAKE hlsl2metal_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/metal ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/spirv-tools/include ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/smol-v/source
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/engine/drv/drv3d_Metal
  COMPILE_DEFINITIONS PRIVATE
    _CROSS_TARGET_METAL BINDUMP_TARGET_BE=0 _CRT_SECURE_NO_DEPRECATE _HAS_EXCEPTIONS=0 _SECURE_SCL=0 EXCLUDE_PSTDINT
    ENABLE_HLSL
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE
    3rdPartyLibs.hash 3rdPartyLibs.vulkan.smol-v 3rdPartyLibs.metal.spirv2Metal 3rdPartyLibs.eastl
    3rdPartyLibs.vulkan.spirv-tools gameLibs.spirv
)
