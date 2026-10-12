# SMOL-V: a smaller, more compressible encoding of SPIR-V shader programs
set(includes source)
set(sources source/smolv.cpp)
if(WIN32)
  set(defines WIN32 NDEBUG _CONSOLE GENERIC_COMPILER YYDEBUG=0)
  set(options /d2Zi+)
endif()

dagor_add_library(3rdPartyLibs.vulkan.smol-v LAX ${sources})
target_include_directories(3rdPartyLibs.vulkan.smol-v PRIVATE ${includes})
target_compile_definitions(3rdPartyLibs.vulkan.smol-v PRIVATE ${defines})
target_compile_options(3rdPartyLibs.vulkan.smol-v PRIVATE ${options})
