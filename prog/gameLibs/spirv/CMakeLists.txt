# SPIR-V tooling of the shader compilers: compiling HLSL with DXC and the passes that fix up its SPIR-V for the engine
find_package(DXC REQUIRED)
if(WIN32)
  list(APPEND libs System::ole32)
endif()
set(defines _CROSS_TARGET_SPIRV)
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND options -Wno-switch -Wno-ambiguous-reversed-operator -Wno-deprecated-declarations)
endif()
if(LINUX AND CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND defines __EMULATE_UUID)
  list(APPEND options
    -Wno-sometimes-uninitialized
    -Wno-switch
    -Wno-ambiguous-reversed-operator
    -Wno-deprecated-declarations
  )
endif()

dagor_add_target(NAME gameLibs.spirv STATIC LAX
  FILES_CMAKE spirv_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/include ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/spirv-tools/include
  COMPILE_DEFINITIONS PRIVATE ${defines}
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES
    PUBLIC ${libs}
    PRIVATE 3rdPartyLibs.vulkan.spirv-tools DXC::DXC
)
