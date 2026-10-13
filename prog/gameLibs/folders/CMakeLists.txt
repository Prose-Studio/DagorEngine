# The well-known folders of a platform (documents, local app data, temp, the executable's), for games and tools
dagor_add_target(NAME gameLibs.folders STATIC LAX
  FILES_CMAKE folders_files.cmake
)
