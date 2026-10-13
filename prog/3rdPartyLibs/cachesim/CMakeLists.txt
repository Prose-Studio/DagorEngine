dagor_add_target(NAME 3rdPartyLibs.cachesim STATIC LAX
  FILES_CMAKE cachesim_files.cmake
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.udis86 System::kernel32 System::psapi
)
