# SPIRV-Cross, the SPIR-V to Metal Shading Language translator of the Metal shader compiler
set(sources
  spirv_cfg.cpp
  spirv_cross.cpp
  spirv_cross_parsed_ir.cpp
  spirv_parser.cpp
  spirv_cpp.cpp
  spirv_glsl.cpp
  spirv_msl.cpp
)
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  set(options
    -Wno-deprecated-declarations
    -Wno-overriding-t-option
    -fno-fast-math
    -Wno-deprecated-this-capture
  )
endif()

dagor_add_library(3rdPartyLibs.metal.spirv2Metal LAX ${sources})
target_compile_options(3rdPartyLibs.metal.spirv2Metal PRIVATE ${options})
