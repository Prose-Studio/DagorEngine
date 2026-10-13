# The embedded browser's host side (Windows): starts the CEF process (helper/, cefprocess.exe next to the program) and
# talks to it over a socket (FlatBuffers messages, lib/ipc/msg) and shared memory (the rendered view)
dagor_add_target(NAME 1stPartyLibs.webbrowser STATIC
  FILES_CMAKE webbrowser_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/flatbuffers/include
  COMPILE_DEFINITIONS PRIVATE UNICODE _UNICODE
  # (MSVC) the pragma pops of flatbuffers.h; the deleted default constructors of the generated messages
  COMPILE_OPTIONS PRIVATE $<$<CXX_COMPILER_ID:MSVC>:/wd5031 /wd4623>
  BUILD_DEPENDENCIES PUBLIC System::ws2_32 System::rpcrt4
)
