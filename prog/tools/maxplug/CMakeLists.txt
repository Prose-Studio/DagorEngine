# The Dagor plugin of 3ds Max (dagor.dlu: the DAG exporter and importer, materials, animations, the tools panels), for
# DAGOR_MAX_VERSION into tools/dagor_cdk/windows-x86_64/plugins-3dsMax/<version>, on the DLL CRT as Max wants it.
# The Max SDK is proprietary: without it (MaxSDK_ROOT) the plugin is skipped. Max 2023/2024 need the VS 2019 toolset
# (the windows-vc16-maxplug preset), Max 2025 and later VS 2022 (windows-maxplug).
find_package(MaxSDK)
if(NOT MaxSDK_FOUND)
  message(STATUS "tools/maxplug: no 3ds Max SDK (MaxSDK_ROOT) for ${DAGOR_MAX_VERSION}: the plugin is skipped")
  return()
endif()
dagor_add_target(NAME dagor SHARED LAX NO_CONFIG_POSTFIX
  OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/dagor_cdk/windows-x86_64/plugins-3dsMax/${DAGOR_MAX_VERSION}
  FILES_CMAKE maxplug_files.cmake
  INCLUDE_DIRECTORIES PRIVATE stubInclude
  COMPILE_DEFINITIONS PRIVATE _UNICODE UNICODE NOMINMAX
  LINK_OPTIONS PRIVATE /DEF:${CMAKE_CURRENT_SOURCE_DIR}/dagor.def
  BUILD_DEPENDENCIES PRIVATE
    MaxSDK::MaxSDK System::kernel32 System::user32 System::gdi32 System::winspool System::comdlg32 System::advapi32
    System::shell32 System::ole32 System::oleaut32 System::uuid System::odbc32 System::odbccp32 System::comctl32
    System::winmm
  FORCE_INCLUDES max_cpt.h
  PROPERTIES SUFFIX .dlu
)
