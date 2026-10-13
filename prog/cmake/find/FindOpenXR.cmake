# Khronos OpenXR loader (Windows x64 and arm64, Android arm64-v8a).
#   OpenXR::OpenXR  the OpenXR headers (<openxr/openxr.h>) and the loader (openxr_loader.dll's import library, or
#                   libopenxr_loader.so); the programs that link it get the loader next to them, on Windows arm64 (a UWP
#                   build) with the forwarders of the UWP C++ runtime to the desktop one
#   OpenXR_VERSION  the version of its headers (XR_CURRENT_API_VERSION), e.g. 1.1.54
# OpenXR_ROOT: a local copy of the release's loader package, unpacked: openxr_loader_windows-<version>.zip, on Android
# openxr_loader_for_android-<version>.aar (default: the pinned one, fetched). VCRTForwarders_ROOT: a local copy of the
# Microsoft.VCRTForwarders.140 NuGet package (Windows arm64).
include(DagorFetch)
if(ANDROID)
  dagor_sdk_root(OpenXR openxr_android)
  find_path(OpenXR_INCLUDE_DIR openxr/openxr.h PATHS "${OpenXR_ROOT}/prefab/modules/headers/include" NO_DEFAULT_PATH)
  find_file(OpenXR_LIBRARY libopenxr_loader.so PATHS "${OpenXR_ROOT}/jni/arm64-v8a" NO_DEFAULT_PATH)
  set(OpenXR_RUNTIME "${OpenXR_LIBRARY}")
  set(_oxr_runtime ".|${OpenXR_LIBRARY}")
  set(_oxr_license "${OpenXR_ROOT}/META-INF/LICENSE")
else()
  dagor_sdk_root(OpenXR openxr)
  set(_oxr_dir "${OpenXR_ROOT}/x64")
  set(_oxr_runtime)
  if(DAGOR_ARCH STREQUAL "arm64")
    set(_oxr_dir "${OpenXR_ROOT}/ARM64_uwp")
    dagor_sdk_root(VCRTForwarders vcrtforwarders)
    set(_oxr_fwd "${VCRTForwarders_ROOT}/runtimes/win-arm64/native/release")
    list(APPEND _oxr_runtime ".|${_oxr_fwd}/msvcp140_app.dll" ".|${_oxr_fwd}/vcruntime140_app.dll")
  endif()
  find_path(OpenXR_INCLUDE_DIR openxr/openxr.h PATHS "${OpenXR_ROOT}/include" NO_DEFAULT_PATH)
  find_file(OpenXR_LIBRARY openxr_loader.lib PATHS "${_oxr_dir}/lib" NO_DEFAULT_PATH)
  find_file(OpenXR_RUNTIME openxr_loader.dll PATHS "${_oxr_dir}/bin" NO_DEFAULT_PATH)
  list(APPEND _oxr_runtime ".|${OpenXR_RUNTIME}")
  if(EXISTS "${_oxr_dir}/bin/openxr_loader.pdb")
    list(APPEND _oxr_runtime ".|${_oxr_dir}/bin/openxr_loader.pdb")
  endif()
  set(_oxr_license "${OpenXR_ROOT}/share/doc/openxr/LICENSE")
endif()
if(OpenXR_INCLUDE_DIR)
  file(STRINGS "${OpenXR_INCLUDE_DIR}/openxr/openxr.h" _oxr_version REGEX "#define XR_CURRENT_API_VERSION ")
  if(_oxr_version MATCHES "XR_MAKE_VERSION\\(([0-9]+), *([0-9]+), *([0-9]+)\\)")
    set(OpenXR_VERSION "${CMAKE_MATCH_1}.${CMAKE_MATCH_2}.${CMAKE_MATCH_3}")
  endif()
endif()
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(OpenXR REQUIRED_VARS OpenXR_LIBRARY OpenXR_RUNTIME OpenXR_INCLUDE_DIR
  VERSION_VAR OpenXR_VERSION)
if(OpenXR_FOUND AND NOT TARGET OpenXR::OpenXR)
  add_library(OpenXR::OpenXR UNKNOWN IMPORTED GLOBAL)
  set_target_properties(OpenXR::OpenXR PROPERTIES IMPORTED_LOCATION "${OpenXR_LIBRARY}"
    INTERFACE_INCLUDE_DIRECTORIES "${OpenXR_INCLUDE_DIR}"
    TRANSITIVE_LINK_PROPERTIES "DAGOR_RUNTIME_FILES;DAGOR_LICENSE_FILES"
    INTERFACE_DAGOR_RUNTIME_FILES "${_oxr_runtime}" INTERFACE_DAGOR_LICENSE_FILES "${_oxr_license}")
endif()
unset(_oxr_dir)
unset(_oxr_fwd)
unset(_oxr_runtime)
unset(_oxr_license)
unset(_oxr_version)
