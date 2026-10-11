# NVIDIA Nsight Aftermath (Windows x64): sdk::aftermath, its headers and HAS_AFTERMATH (the drivers load the library
# when it is there)
set(DAGOR_SDK_AFTERMATH_ROOT "")
if(DAGOR_PLATFORM STREQUAL "windows" AND DAGOR_ARCH STREQUAL "x86_64")
  dagor_fetch_sdk(aftermath DAGOR_SDK_AFTERMATH_ROOT)
  add_library(sdk::aftermath INTERFACE IMPORTED GLOBAL)
  set_target_properties(sdk::aftermath PROPERTIES
    INTERFACE_INCLUDE_DIRECTORIES "${DAGOR_SDK_AFTERMATH_ROOT}/include"
    INTERFACE_COMPILE_DEFINITIONS HAS_AFTERMATH)
endif()
