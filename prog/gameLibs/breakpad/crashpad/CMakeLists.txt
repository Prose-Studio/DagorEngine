# The crash reports of Crashpad (Windows; the other platforms link gameLibs/breakpad/stub)
dagor_add_target(NAME gameLibs.breakpad.crashpad STATIC LAX
  FILES_CMAKE crashpad_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/crashpad
    ${DAGOR_PROG_DIR}/3rdPartyLibs/crashpad/third_party/mini_chromium/mini_chromium
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.crashpad
)
