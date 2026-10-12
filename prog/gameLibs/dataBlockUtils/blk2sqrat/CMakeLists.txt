dagor_add_target(NAME gameLibs.dataBlockUtils.blk2sqrat STATIC
  FILES_CMAKE blk2sqrat_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR}
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)
