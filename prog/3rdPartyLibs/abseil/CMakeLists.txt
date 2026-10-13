dagor_add_target(NAME 3rdPartyLibs.abseil STATIC LAX
  FILES_CMAKE abseil_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
)
