# AMD FidelityFX SDK (Windows x64).
#   FidelityFX::FidelityFX  the headers of its API, upscalers and frame generation; the programs that link it get the
#                           signed DX12 DLLs next to them (the driver loads them)
# FidelityFX_ROOT: a local copy (default: the pinned one, fetched).
include(DagorFetch)
dagor_sdk_root(FidelityFX fidelityfx)
set(_ffx "${FidelityFX_ROOT}/Kits/FidelityFX")
find_path(FidelityFX_INCLUDE_DIR ffx_api.h PATHS "${_ffx}/api/include" NO_DEFAULT_PATH)
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(FidelityFX REQUIRED_VARS FidelityFX_INCLUDE_DIR)
if(FidelityFX_FOUND AND NOT TARGET FidelityFX::FidelityFX)
  add_library(FidelityFX::FidelityFX INTERFACE IMPORTED GLOBAL)
  set(_dlls loader framegeneration upscaler)
  list(TRANSFORM _dlls REPLACE "^(.*)$" ".|${_ffx}/signedbin/amd_fidelityfx_\\1_dx12.dll")
  set_target_properties(FidelityFX::FidelityFX PROPERTIES
    INTERFACE_INCLUDE_DIRECTORIES "${_ffx};${_ffx}/api/include;${_ffx}/framegeneration/include;${_ffx}/upscalers/include"
    TRANSITIVE_LINK_PROPERTIES DAGOR_RUNTIME_FILES INTERFACE_DAGOR_RUNTIME_FILES "${_dlls}")
  unset(_dlls)
endif()
unset(_ffx)
