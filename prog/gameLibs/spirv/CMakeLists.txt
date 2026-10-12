# SPIR-V tooling of the shader compilers: compiling HLSL with DXC and the passes that fix up its SPIR-V for the engine
list(APPEND sources
  traits_table.cpp
  module_writer.cpp
  module_reader.cpp
  module_builder.cpp
  atomic_counter_resolve_pass.cpp
  compile_header_pass.cpp
  buffer_unique_pointer_pass.cpp
  dxc_bugfix_pass.cpp
  rename_entry_points_pass.cpp
  semantic_resolve_pass.cpp
  structure_layout_validation_pass.cpp
  reflection_cleanup_pass.cpp
  compiler_dxc.cpp
)
list(APPEND includes
  ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/spirv-tools/include
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
find_package(DXC REQUIRED)
list(APPEND deps 3rdPartyLibs.vulkan.spirv-tools DXC::DXC)
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

dagor_add_library(gameLibs.spirv LAX ${sources})
target_include_directories(gameLibs.spirv PRIVATE ${includes})
target_compile_definitions(gameLibs.spirv PRIVATE ${defines})
target_compile_options(gameLibs.spirv PRIVATE ${options})
target_link_libraries(gameLibs.spirv PRIVATE ${deps})
target_link_libraries(gameLibs.spirv PUBLIC ${libs})
