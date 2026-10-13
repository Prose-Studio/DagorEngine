dagor_add_target(NAME gameLibs.daPhys STATIC
  FILES_CMAKE daPhys_files.cmake
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.regExp
)
