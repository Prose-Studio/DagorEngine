# The disassembler of compiled shader blobs (SPIR-V through spirv-tools, DXIL on Windows), for shaderInfo and the
# shader compilers' debug output
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(deps 3rdPartyLibs.regExp 3rdPartyLibs.vulkan.spirv-tools gameLibs.shaderBlobUnpack)
if(CMAKE_SYSTEM_NAME MATCHES "^(Darwin|Linux|Windows)$")
  list(APPEND includes
    ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/spirv-tools/include
  )
  if(WIN32)
    list(APPEND deps gameLibs.dxil)
  endif()
else()
  message(FATAL_ERROR "tools/ShaderCompiler2/shaderBlobDisassembler does not support ${DAGOR_PLATFORM}")
endif()

dagor_add_target(NAME tools.ShaderCompiler2.shaderBlobDisassembler STATIC LAX
  FILES_CMAKE shaderBlobDisassembler_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
