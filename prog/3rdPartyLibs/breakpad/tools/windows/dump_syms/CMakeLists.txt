# breakpad's dump_syms: the symbol files of programs for the crash reports (tools/util), on the DIA SDK and ATL
dagor_add_target(NAME dump_syms EXECUTABLE LAX OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/util
  FILES_CMAKE dump_syms_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/breakpad ${DAGOR_PROG_DIR}/3rdPartyLibs/diasdk/include ${DAGOR_MSVC_DIR}/atlmfc/include
  COMPILE_DEFINITIONS PRIVATE
    __B_NO_MEM_BASE_INCLUDE UNICODE _SILENCE_STDEXT_HASH_DEPRECATION_WARNINGS _ATL_ALLOW_CHAR_UNSIGNED
  LINK_OPTIONS PRIVATE -ignore:4254
  BUILD_DEPENDENCIES PRIVATE
    3rdPartyLibs.breakpad.common.windows System::wininet System::version System::imagehlp
    ${DAGOR_PROG_DIR}/3rdPartyLibs/diasdk/lib/amd64/diaguids.lib ${DAGOR_MSVC_DIR}/atlmfc/lib/x64/atls.lib
  LICENSES ${DAGOR_PROG_DIR}/3rdPartyLibs/breakpad
  PROPERTIES DAGOR_EXCEPTIONS SEH DAGOR_RTTI ON
)
