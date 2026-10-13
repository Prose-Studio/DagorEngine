# NVIDIA NVAPI (Windows).
#   NVAPI::NVAPI  its headers and the library of the target arch, and HAS_NVAPI
# Not found where the SDK has no library for the arch (arm64 in R610): its users build without it.
# NVAPI_ROOT: a local copy (default: the pinned one, fetched).
include(DagorFetch)
dagor_sdk_root(NVAPI nvapi)
if(DAGOR_ARCH STREQUAL "x86_64")
  set(_nvapi_lib amd64/nvapi64.lib)
else()
  set(_nvapi_lib aarch64/nvapia64.lib)
endif()
find_path(NVAPI_INCLUDE_DIR nvapi.h PATHS "${NVAPI_ROOT}" NO_DEFAULT_PATH NO_CMAKE_FIND_ROOT_PATH)
find_file(NVAPI_LIBRARY ${_nvapi_lib} PATHS "${NVAPI_ROOT}" NO_DEFAULT_PATH NO_CMAKE_FIND_ROOT_PATH)
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(NVAPI REQUIRED_VARS NVAPI_LIBRARY NVAPI_INCLUDE_DIR)
if(NVAPI_FOUND AND NOT TARGET NVAPI::NVAPI)
  add_library(NVAPI::NVAPI STATIC IMPORTED GLOBAL)
  set_target_properties(NVAPI::NVAPI PROPERTIES IMPORTED_LOCATION "${NVAPI_LIBRARY}"
    INTERFACE_INCLUDE_DIRECTORIES "${NVAPI_INCLUDE_DIR}" INTERFACE_COMPILE_DEFINITIONS HAS_NVAPI)
endif()
unset(_nvapi_lib)
