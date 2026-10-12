dagor_add_target(NAME gameLibs.gesture STATIC
  FILES_CMAKE gesture_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
