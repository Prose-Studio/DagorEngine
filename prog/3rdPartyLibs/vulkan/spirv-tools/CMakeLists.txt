# SPIRV-Tools (Khronos): the SPIR-V assembler, disassembler, validator and optimizer; replaces its upstream CMakeLists
set(defines NDEBUG _CONSOLE GENERIC_COMPILER YYDEBUG=0)
if(WIN32)
  list(APPEND defines WIN32)
  list(APPEND options /d2Zi+)
endif()
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND options -Wno-deprecated-declarations)
endif()

dagor_add_target(NAME 3rdPartyLibs.vulkan.spirv-tools STATIC LAX
  FILES_CMAKE spirv-tools_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR} include source source/opt source/util source/val external/spirv-headers/include
    external/spirv-headers/include/spirv/unified1
  COMPILE_DEFINITIONS PRIVATE ${defines}
  COMPILE_OPTIONS PRIVATE ${options}
)
