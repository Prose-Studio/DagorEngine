# Microsoft DirectX Shader Compiler (dxcompiler, dxil), which the shader compilers load at run time.
#   DXC::DXC               its headers (<dxc/dxcapi.h>) and the licenses of its libraries
#   DXC_RUNTIME_LIBRARIES  the libraries a program loads it from, for dagor_target_runtime_files() (the programs differ in
#                          the dir they look in)
# DXC_ROOT: a local copy of the release (default: the pinned one, fetched).
include(DagorFetch)
dagor_sdk_root(DXC dxc)
if(WIN32)
  # the Windows release has its headers in inc/; the code includes them as <dxc/...>
  if(NOT EXISTS "${DXC_ROOT}/include/dxc/dxcapi.h" AND EXISTS "${DXC_ROOT}/inc/dxcapi.h")
    file(COPY "${DXC_ROOT}/inc/" DESTINATION "${DXC_ROOT}/include/dxc")
  endif()
  string(REPLACE "x86_64" "x64" _dxc_arch "${DAGOR_ARCH}")
  set(_dxc_runtime "${DXC_ROOT}/bin/${_dxc_arch}/dxcompiler.dll" "${DXC_ROOT}/bin/${_dxc_arch}/dxil.dll")
  file(GLOB _dxc_licenses "${DXC_ROOT}/LICENSE-*.txt")
elseif(APPLE)
  set(_dxc_runtime "${DXC_ROOT}/lib/macosx/dxcompiler.dylib" "${DXC_ROOT}/lib/macosx/dxil.dylib")
  set(_dxc_licenses "${DXC_ROOT}/LICENSE.TXT")
else()
  set(_dxc_runtime "${DXC_ROOT}/lib/libdxcompiler.so" "${DXC_ROOT}/lib/libdxil.so")
  file(GLOB _dxc_licenses "${DXC_ROOT}/LICENSE-*.txt")
endif()
find_path(DXC_INCLUDE_DIR dxc/dxcapi.h PATHS "${DXC_ROOT}/include" NO_DEFAULT_PATH)
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(DXC REQUIRED_VARS DXC_INCLUDE_DIR)
if(DXC_FOUND AND NOT TARGET DXC::DXC)
  add_library(DXC::DXC INTERFACE IMPORTED GLOBAL)
  set_target_properties(DXC::DXC PROPERTIES INTERFACE_INCLUDE_DIRECTORIES "${DXC_INCLUDE_DIR}"
    TRANSITIVE_LINK_PROPERTIES DAGOR_LICENSE_FILES INTERFACE_DAGOR_LICENSE_FILES "${_dxc_licenses}")
endif()
set(DXC_RUNTIME_LIBRARIES ${_dxc_runtime})
unset(_dxc_arch)
unset(_dxc_runtime)
unset(_dxc_licenses)
