dagor_add_target(NAME gameLibs.dataBlockUtils.blk2sqrat STATIC
  FILES_CMAKE blk2sqrat_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)
