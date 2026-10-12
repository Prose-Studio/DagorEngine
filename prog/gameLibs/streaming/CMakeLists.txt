dagor_add_target(NAME gameLibs.streaming STATIC
  FILES_CMAKE streaming_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
