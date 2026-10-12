# NVIDIA Nsight Aftermath (Windows x64).
#   Aftermath::Aftermath  its headers and HAS_AFTERMATH (the drivers load the library when it is there)
# Aftermath_ROOT: a local copy (default: the pinned one, fetched).
include(DagorFetch)
dagor_sdk_root(Aftermath aftermath)
find_path(Aftermath_INCLUDE_DIR GFSDK_Aftermath.h PATHS "${Aftermath_ROOT}/include" NO_DEFAULT_PATH)
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(Aftermath REQUIRED_VARS Aftermath_INCLUDE_DIR)
if(Aftermath_FOUND AND NOT TARGET Aftermath::Aftermath)
  add_library(Aftermath::Aftermath INTERFACE IMPORTED GLOBAL)
  set_target_properties(Aftermath::Aftermath PROPERTIES INTERFACE_INCLUDE_DIRECTORIES "${Aftermath_INCLUDE_DIR}"
    INTERFACE_COMPILE_DEFINITIONS HAS_AFTERMATH)
endif()
