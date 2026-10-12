# ISO 8601 time parsing and formatting
add_subdirectory(tests)

set(includes ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources iso8601Time.cpp)
if(WIN32)
  list(APPEND options /wd4548)
endif()

dagor_add_library(gameLibs.iso8601Time ${sources})
target_include_directories(gameLibs.iso8601Time PRIVATE ${includes})
target_compile_options(gameLibs.iso8601Time PRIVATE ${options})
