# DirectX 12 Agility SDK (Windows).
#   Agility::Agility  its headers (before the Windows SDK's d3d12.h) and d3dx12; the programs that link it get
#                     D3D12Core and D3D12SDKLayers in a D3D12 dir next to them
# Agility_ROOT: a local copy of the NuGet package (default: the pinned one, fetched).
include(DagorFetch)
dagor_sdk_root(Agility agility)
string(REPLACE "x86_64" "x64" _agility_bin "${DAGOR_ARCH}")
set(_agility_bin "${Agility_ROOT}/build/native/bin/${_agility_bin}")
find_path(Agility_INCLUDE_DIR d3d12.h PATHS "${Agility_ROOT}/build/native/include" NO_DEFAULT_PATH)
find_file(Agility_CORE D3D12Core.dll PATHS "${_agility_bin}" NO_DEFAULT_PATH)
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(Agility REQUIRED_VARS Agility_INCLUDE_DIR Agility_CORE)
if(Agility_FOUND AND NOT TARGET Agility::Agility)
  add_library(Agility::Agility INTERFACE IMPORTED GLOBAL)
  set_target_properties(Agility::Agility PROPERTIES
    INTERFACE_INCLUDE_DIRECTORIES "${Agility_INCLUDE_DIR};${Agility_INCLUDE_DIR}/d3dx12"
    TRANSITIVE_LINK_PROPERTIES DAGOR_RUNTIME_FILES
    INTERFACE_DAGOR_RUNTIME_FILES "D3D12|${Agility_CORE};D3D12|${_agility_bin}/d3d12SDKLayers.dll")
endif()
unset(_agility_bin)
