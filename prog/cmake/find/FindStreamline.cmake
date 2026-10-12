# NVIDIA Streamline (DLSS, Reflex), user-provided: Streamline_ROOT is the unpacked SDK (include/, lib/x64).
#   Streamline::Streamline  its headers and interposer library
find_path(Streamline_INCLUDE_DIR sl.h PATH_SUFFIXES include)
find_library(Streamline_LIBRARY sl.interposer PATH_SUFFIXES lib/x64)
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(Streamline REQUIRED_VARS Streamline_LIBRARY Streamline_INCLUDE_DIR)
if(Streamline_FOUND AND NOT TARGET Streamline::Streamline)
  add_library(Streamline::Streamline STATIC IMPORTED GLOBAL)
  set_target_properties(Streamline::Streamline PROPERTIES IMPORTED_LOCATION "${Streamline_LIBRARY}"
    INTERFACE_INCLUDE_DIRECTORIES "${Streamline_INCLUDE_DIR}")
endif()
