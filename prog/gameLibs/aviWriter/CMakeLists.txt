dagor_add_target(NAME gameLibs.aviWriter STATIC
  FILES_CMAKE aviWriter_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
)
