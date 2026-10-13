dagor_add_target(NAME gameLibs.profileEventsGUI STATIC
  FILES_CMAKE profileEventsGUI_files.cmake
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
)
