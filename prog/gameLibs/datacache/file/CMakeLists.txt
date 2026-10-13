# Data cache: the file backend
dagor_add_target(NAME gameLibs.datacache.file STATIC
  FILES_CMAKE file_files.cmake
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl gameLibs.datacache.common
)
