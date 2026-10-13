# AMD GPU Services (Windows x64).
#   AGS::AGS  amd_ags.h, the import library of the delay-loaded amd_ags_x64.dll and HAS_AGS; the programs that link it
#             get the DLL next to them
# AGS_ROOT: a local copy (default: the pinned one, fetched).
include(DagorFetch)
dagor_sdk_root(AGS ags)
find_path(AGS_INCLUDE_DIR amd_ags.h PATHS "${AGS_ROOT}/ags_lib/inc" NO_DEFAULT_PATH NO_CMAKE_FIND_ROOT_PATH)
find_file(AGS_LIBRARY amd_ags_x64.lib PATHS "${AGS_ROOT}/ags_lib/lib" NO_DEFAULT_PATH NO_CMAKE_FIND_ROOT_PATH)
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(AGS REQUIRED_VARS AGS_LIBRARY AGS_INCLUDE_DIR)
if(AGS_FOUND AND NOT TARGET AGS::AGS)
  add_library(AGS::AGS STATIC IMPORTED GLOBAL)
  set_target_properties(AGS::AGS PROPERTIES IMPORTED_LOCATION "${AGS_LIBRARY}"
    INTERFACE_INCLUDE_DIRECTORIES "${AGS_INCLUDE_DIR}" INTERFACE_COMPILE_DEFINITIONS HAS_AGS
    INTERFACE_LINK_LIBRARIES System::delayimp INTERFACE_LINK_OPTIONS "/DELAYLOAD:amd_ags_x64.dll"
    TRANSITIVE_LINK_PROPERTIES DAGOR_RUNTIME_FILES INTERFACE_DAGOR_RUNTIME_FILES ".|${AGS_ROOT}/ags_lib/lib/amd_ags_x64.dll")
endif()
