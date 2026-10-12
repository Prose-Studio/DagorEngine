# SPIRV-Cross, the SPIR-V to Metal Shading Language translator of the Metal shader compiler
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  set(options
    -Wno-deprecated-declarations
    -Wno-overriding-t-option
    -fno-fast-math
    -Wno-deprecated-this-capture
  )
endif()

dagor_add_target(NAME 3rdPartyLibs.metal.spirv2Metal STATIC LAX
  FILES_CMAKE spirv2Metal_files.cmake
  COMPILE_OPTIONS PRIVATE ${options}
)
