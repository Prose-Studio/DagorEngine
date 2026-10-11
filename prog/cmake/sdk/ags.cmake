# AMD GPU Services (Windows x64): sdk::ags (amd_ags.h, the import library of the delay-loaded amd_ags_x64.dll,
# HAS_AGS) and DAGOR_SDK_AGS_RUNTIME, the DLL to ship next to the program
set(DAGOR_SDK_AGS_ROOT "")
if(DAGOR_PLATFORM STREQUAL "windows" AND DAGOR_ARCH STREQUAL "x86_64")
  dagor_fetch_sdk(ags _dagor_ags_dir)
  set(DAGOR_SDK_AGS_ROOT "${_dagor_ags_dir}/ags_lib")
  add_library(sdk::ags INTERFACE IMPORTED GLOBAL)
  set_target_properties(sdk::ags PROPERTIES
    INTERFACE_INCLUDE_DIRECTORIES "${DAGOR_SDK_AGS_ROOT}/inc"
    INTERFACE_LINK_LIBRARIES "${DAGOR_SDK_AGS_ROOT}/lib/amd_ags_x64.lib;delayimp"
    INTERFACE_LINK_OPTIONS "/DELAYLOAD:amd_ags_x64.dll"
    INTERFACE_COMPILE_DEFINITIONS HAS_AGS)
  set(DAGOR_SDK_AGS_RUNTIME "${DAGOR_SDK_AGS_ROOT}/lib/amd_ags_x64.dll" CACHE INTERNAL "")
  unset(_dagor_ags_dir)
endif()
