# ISO 8601 time parsing and formatting
if(DAGOR_ENGINE_TESTS)
  add_subdirectory(tests)
endif()
if(WIN32)
  list(APPEND options /wd4548)
endif()

dagor_add_target(NAME gameLibs.iso8601Time STATIC
  FILES_CMAKE iso8601Time_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  COMPILE_OPTIONS PRIVATE ${options}
)
