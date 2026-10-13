# The embedded browser's CEF process (cefprocess.exe, Windows): runs the browser off screen for the host
# (1stPartyLibs.webbrowser), which starts it from its program's dir; CEF's runtime goes next to it
dagor_add_target(NAME cefprocess EXECUTABLE APPLICATION LAX NO_CONFIG_POSTFIX
  FILES_CMAKE helper_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/1stPartyLibs/webbrowser/lib ${DAGOR_PROG_DIR}/3rdPartyLibs/flatbuffers/include
  COMPILE_DEFINITIONS PRIVATE __B_NO_MEM_BASE_INCLUDE UNICODE _UNICODE
  BUILD_DEPENDENCIES PRIVATE 1stPartyLibs.webbrowser 3rdPartyLibs.cef3.v4896.libcef_dll System::shell32
)
