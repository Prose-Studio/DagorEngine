# CEF's C++ wrapper of libcef's C API (libcef_dll_wrapper) and the headers of CEF 100.0.24, on the binaries of that
# version (FindCEF.cmake). Its users compile the headers as it does, with NDEBUG: DCHECK_IS_ON() changes the layout of
# CEF's base classes (include/base/cef_ref_counted.h), which must match the release libcef's.
find_package(CEF 100.0.24 EXACT REQUIRED)
dagor_add_target(NAME 3rdPartyLibs.cef3.v4896.libcef_dll STATIC LAX
  FILES_CMAKE libcef_dll_files.cmake
  INCLUDE_DIRECTORIES PUBLIC ${DAGOR_PROG_DIR}/3rdPartyLibs/cef3/v4896 ${DAGOR_PROG_DIR}/3rdPartyLibs/cef3/v4896/include
  COMPILE_DEFINITIONS PUBLIC NDEBUG PRIVATE WRAPPING_CEF_SHARED UNICODE _UNICODE
  COMPILE_OPTIONS PRIVATE $<$<CXX_COMPILER_ID:Clang>:-Wno-undefined-var-template>
  BUILD_DEPENDENCIES PUBLIC CEF::CEF
)
