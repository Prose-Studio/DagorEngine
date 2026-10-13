# Chromium Embedded Framework: the binaries of a CEF distribution (Windows). Its headers and C++ wrapper are built from
# prog/3rdPartyLibs/cef3/<version>, which must be of the same version.
#   CEF::CEF      the import library of libcef.dll; the programs that link it get CEF's runtime next to them
#   CEF::Runtime  that runtime alone, for the programs that start a CEF process: libcef.dll, the ANGLE, SwiftShader and
#                 Vulkan DLLs, the V8 snapshots, the resources (.pak, ICU data) and locales/
#   CEF_VERSION   the distribution's version (include/cef_version.h), e.g. 100.0.24
# CEF_ROOT: a binary distribution, the dir with Release/ and Resources/ (default: the target's pinned one, fetched).
include(DagorFetch)
dagor_sdk_root(CEF cef OPTIONAL HOST ${DAGOR_PLATFORM}-${DAGOR_ARCH})
find_file(CEF_LIBRARY libcef.lib PATHS "${CEF_ROOT}/Release" NO_DEFAULT_PATH NO_CMAKE_FIND_ROOT_PATH)
find_path(CEF_RESOURCES_DIR icudtl.dat PATHS "${CEF_ROOT}/Resources" NO_DEFAULT_PATH NO_CMAKE_FIND_ROOT_PATH)
set(CEF_VERSION)
if(CEF_ROOT AND EXISTS "${CEF_ROOT}/include/cef_version.h")
  file(STRINGS "${CEF_ROOT}/include/cef_version.h" _cef_version REGEX "^#define CEF_VERSION_(MAJOR|MINOR|PATCH) ")
  string(REGEX REPLACE ".*MAJOR ([0-9]+).*MINOR ([0-9]+).*PATCH ([0-9]+).*" "\\1.\\2.\\3" CEF_VERSION "${_cef_version}")
endif()
set(_cef_reason)
if(NOT CEF_ROOT)
  set(_cef_reason REASON_FAILURE_MESSAGE
    "prog/cmake/sdk/manifest.cmake has no CEF for ${DAGOR_PLATFORM}-${DAGOR_ARCH}: set CEF_ROOT")
endif()
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(CEF REQUIRED_VARS CEF_LIBRARY CEF_RESOURCES_DIR VERSION_VAR CEF_VERSION
  ${_cef_reason})
if(CEF_FOUND AND NOT TARGET CEF::CEF)
  # next to the program, as libcef looks for them; the locales and the software GL in their dirs
  set(_cef_runtime)
  foreach(_cef_entry ".|Release/*.dll" ".|Release/*.bin" ".|Release/*.json" "swiftshader|Release/swiftshader/*.dll"
                     ".|Resources/*.pak" ".|Resources/*.dat" "locales|Resources/locales/*.pak")
    string(REPLACE "|" ";" _cef_entry "${_cef_entry}")
    list(GET _cef_entry 0 _cef_dir)
    list(GET _cef_entry 1 _cef_glob)
    file(GLOB _cef_files "${CEF_ROOT}/${_cef_glob}")
    list(TRANSFORM _cef_files PREPEND "${_cef_dir}|")
    list(APPEND _cef_runtime ${_cef_files})
  endforeach()
  add_library(CEF::Runtime INTERFACE IMPORTED GLOBAL)
  set_target_properties(CEF::Runtime PROPERTIES
    TRANSITIVE_LINK_PROPERTIES "DAGOR_RUNTIME_FILES;DAGOR_LICENSE_FILES" INTERFACE_DAGOR_RUNTIME_FILES "${_cef_runtime}"
    INTERFACE_DAGOR_LICENSE_FILES "${CEF_ROOT}/LICENSE.txt")
  add_library(CEF::CEF SHARED IMPORTED GLOBAL)
  set_target_properties(CEF::CEF PROPERTIES IMPORTED_IMPLIB "${CEF_LIBRARY}"
    IMPORTED_LOCATION "${CEF_ROOT}/Release/libcef.dll" INTERFACE_LINK_LIBRARIES CEF::Runtime)
endif()
unset(_cef_version)
unset(_cef_reason)
unset(_cef_runtime)
unset(_cef_entry)
unset(_cef_dir)
unset(_cef_glob)
unset(_cef_files)
