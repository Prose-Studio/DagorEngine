# FLTK (fltk.org), the GUI toolkit of bpreport's dialog and of the Linux message box.
#   FLTK::FLTK    its core library. Windows, macOS: built in the tree from FLTK's source by its own CMake, static,
#                 with the tree's compiler, flags and C runtime (no fluid, tests or docs); on Windows it has the
#                 WinMain that calls a GUI program's main(). Linux: the distro's (System::fltk, looked up and reported
#                 missing with the other system libraries), with X11
#   FLTK_VERSION  the version of the source (Windows, macOS)
# FLTK_ROOT: Windows, macOS: a local copy of FLTK's source release (default: the pinned one, fetched).
if(LINUX)
  if(NOT TARGET FLTK::FLTK)
    add_library(FLTK::FLTK INTERFACE IMPORTED GLOBAL)
    set_property(TARGET FLTK::FLTK PROPERTY INTERFACE_LINK_LIBRARIES System::fltk System::X11)
    if(IS_DIRECTORY /usr/include/cairo) # the distro's FLTK headers include cairo's
      set_property(TARGET FLTK::FLTK PROPERTY INTERFACE_INCLUDE_DIRECTORIES /usr/include/cairo)
    endif()
  endif()
  set(FLTK_FOUND TRUE)
  return()
endif()

include(DagorFetch)
dagor_sdk_root(FLTK fltk)
find_path(FLTK_INCLUDE_DIR FL/Fl.H PATHS "${FLTK_ROOT}" NO_DEFAULT_PATH NO_CMAKE_FIND_ROOT_PATH) # the source's root
if(FLTK_INCLUDE_DIR)
  file(STRINGS "${FLTK_INCLUDE_DIR}/FL/Enumerations.H" _fltk_version
    REGEX "^#define FL_(MAJOR|MINOR|PATCH)_VERSION[ \t]+[0-9]+")
  string(REGEX MATCHALL "[0-9]+" _fltk_version "${_fltk_version}")
  list(JOIN _fltk_version "." FLTK_VERSION)
endif()
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(FLTK REQUIRED_VARS FLTK_INCLUDE_DIR VERSION_VAR FLTK_VERSION)
if(FLTK_FOUND AND NOT TARGET FLTK::FLTK)
  block()
    foreach(_part FLUID FLTK_OPTIONS TEST EXAMPLES FORMS GL HTML_DOCS PDF_DOCS SHARED_LIBS)
      set(FLTK_BUILD_${_part} OFF)
    endforeach()
    set(FLTK_MSVC_RUNTIME_DLL OFF)
    # FLTK's own conventions: system libraries linked by name, warnings that are not errors, no configuration summary;
    # the Find modules it includes are not part of this find_package
    set(CMAKE_LINK_LIBRARIES_ONLY_TARGETS OFF)
    set(CMAKE_COMPILE_WARNING_AS_ERROR OFF)
    set(CMAKE_MESSAGE_LOG_LEVEL WARNING)
    unset(CMAKE_FIND_PACKAGE_NAME)
    add_subdirectory("${FLTK_INCLUDE_DIR}" "${CMAKE_BINARY_DIR}/fltk" EXCLUDE_FROM_ALL SYSTEM)
  endblock()
  # the tree's C runtime in every configuration (FLTK picks the debug one for a configuration named Debug only); the
  # program's operator new and delete rather than the engine's inline ones (dag_memBase.h); on Windows without the
  # engine's NOMINMAX (GDI+ uses windows.h's min and max) and WIN32_LEAN_AND_MEAN, which FLTK defines itself
  if(MSVC)
    set_property(TARGET fltk PROPERTY MSVC_RUNTIME_LIBRARY "${CMAKE_MSVC_RUNTIME_LIBRARY}")
  endif()
  target_compile_definitions(fltk PRIVATE __B_NO_MEM_BASE_INCLUDE)
  if(WIN32)
    get_property(_fltk_defs DIRECTORY "${FLTK_INCLUDE_DIR}/src" PROPERTY COMPILE_DEFINITIONS)
    list(FILTER _fltk_defs EXCLUDE REGEX ":(NOMINMAX|WIN32_LEAN_AND_MEAN=)>$")
    set_property(DIRECTORY "${FLTK_INCLUDE_DIR}/src" PROPERTY COMPILE_DEFINITIONS "${_fltk_defs}")
    # the system libraries its code calls beyond those its CMake names, which come from CMake's default link line
    # (CMAKE_CXX_STANDARD_LIBRARIES, empty in the tree)
    target_link_libraries(fltk INTERFACE System::comdlg32 System::shell32 System::winspool)
  endif()
  set_target_properties(fltk PROPERTIES TRANSITIVE_LINK_PROPERTIES DAGOR_LICENSE_FILES
    INTERFACE_DAGOR_LICENSE_FILES "${FLTK_INCLUDE_DIR}/COPYING")
  add_library(FLTK::FLTK ALIAS fltk)
endif()
unset(_fltk_version)
unset(_fltk_defs)
