# Tools utilities: strings, file paths and masks, hashing, undo system, log writers, BLK helpers, binary dumps
if(NOT WIN32 AND LINUX)
  list(APPEND libs System::uuid)
endif()

dagor_add_target(NAME tools.libTools.util STATIC LAX
  FILES_CMAKE util_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sharedInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES
    PUBLIC ${libs}
    PRIVATE 3rdPartyLibs.hash 3rdPartyLibs.regExp
)
