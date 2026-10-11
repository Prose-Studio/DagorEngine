# AMD FidelityFX SDK (Windows x64): sdk::fidelityfx, the headers of its API, upscalers and frame generation, and
# DAGOR_SDK_FIDELITYFX_RUNTIME, the signed DLLs of DX12 to ship next to the program (the driver loads them)
set(DAGOR_SDK_FIDELITYFX_ROOT "")
if(DAGOR_PLATFORM STREQUAL "windows" AND DAGOR_ARCH STREQUAL "x86_64")
  dagor_fetch_sdk(fidelityfx _dagor_ffx_dir)
  set(DAGOR_SDK_FIDELITYFX_ROOT "${_dagor_ffx_dir}/Kits/FidelityFX")
  add_library(sdk::fidelityfx INTERFACE IMPORTED GLOBAL)
  set_target_properties(sdk::fidelityfx PROPERTIES INTERFACE_INCLUDE_DIRECTORIES
    "${DAGOR_SDK_FIDELITYFX_ROOT};${DAGOR_SDK_FIDELITYFX_ROOT}/api/include;${DAGOR_SDK_FIDELITYFX_ROOT}/framegeneration/include;${DAGOR_SDK_FIDELITYFX_ROOT}/upscalers/include")
  set(_dagor_ffx_bin "${DAGOR_SDK_FIDELITYFX_ROOT}/signedbin")
  set(DAGOR_SDK_FIDELITYFX_RUNTIME "${_dagor_ffx_bin}/amd_fidelityfx_loader_dx12.dll"
    "${_dagor_ffx_bin}/amd_fidelityfx_framegeneration_dx12.dll" "${_dagor_ffx_bin}/amd_fidelityfx_upscaler_dx12.dll"
    CACHE INTERNAL "")
  unset(_dagor_ffx_dir)
  unset(_dagor_ffx_bin)
endif()
