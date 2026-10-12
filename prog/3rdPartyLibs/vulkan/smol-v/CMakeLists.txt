# SMOL-V: a smaller, more compressible encoding of SPIR-V shader programs
if(WIN32)
  set(defines WIN32 NDEBUG _CONSOLE GENERIC_COMPILER YYDEBUG=0)
  set(options /d2Zi+)
endif()

dagor_add_target(NAME 3rdPartyLibs.vulkan.smol-v STATIC LAX
  FILES_CMAKE smol-v_files.cmake
  INCLUDE_DIRECTORIES PRIVATE source
  COMPILE_DEFINITIONS PRIVATE ${defines}
  COMPILE_OPTIONS PRIVATE ${options}
)
