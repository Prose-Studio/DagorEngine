# System information (OS, CPU, GPU and memory) for logs and crash reports; a stub where a platform has none
if(WIN32)
  list(APPEND includes ${DAGOR_ENGINE_ROOT}/3rdPartyLibs/eastl/include)
  list(APPEND libs System::advapi32)
endif()

dagor_add_target(NAME 1stPartyLibs.sysinfo STATIC
  FILES_CMAKE sysinfo_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  BUILD_DEPENDENCIES PUBLIC ${libs}
)
