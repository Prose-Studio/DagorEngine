# The Dagor plugin of 3ds Max (dagor.dlu: the DAG exporter and importer, materials, animations, the tools panels), for
# each 3ds Max SDK found (2025 and later, FindMaxSDK.cmake) into tools/dagor_cdk/windows-x86_64/plugins-3dsMax/Max<version>,
# on the DLL CRT as Max wants it. The Max SDK is proprietary: without one the plugin is skipped.
find_package(MaxSDK)
if(NOT MaxSDK_FOUND)
  message(STATUS "tools/maxplug: no 3ds Max SDK of ${DAGOR_MAX_VERSIONS} (MaxSDK_<version>_ROOT): the plugin is skipped")
  return()
endif()
foreach(version IN LISTS MaxSDK_VERSIONS)
  dagor_add_target(NAME dagor-max${version} SHARED LAX NO_CONFIG_POSTFIX OUTPUT_NAME dagor
    OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/dagor_cdk/windows-x86_64/plugins-3dsMax/Max${version}
    FILES_CMAKE maxplug_files.cmake
    INCLUDE_DIRECTORIES PRIVATE stubInclude
    COMPILE_DEFINITIONS PRIVATE _UNICODE UNICODE NOMINMAX
    LINK_OPTIONS PRIVATE /DEF:${CMAKE_CURRENT_SOURCE_DIR}/dagor.def
    BUILD_DEPENDENCIES PRIVATE
      MaxSDK::${version} System::kernel32 System::user32 System::gdi32 System::winspool System::comdlg32 System::advapi32
      System::shell32 System::ole32 System::oleaut32 System::uuid System::odbc32 System::odbccp32 System::comctl32
      System::winmm
    FORCE_INCLUDES max_cpt.h
    PROPERTIES SUFFIX .dlu
  )
endforeach()
