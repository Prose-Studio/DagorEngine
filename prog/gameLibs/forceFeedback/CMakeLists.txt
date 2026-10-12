dagor_add_target(NAME gameLibs.forceFeedback STATIC
  FILES_CMAKE forceFeedback_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR}
)
