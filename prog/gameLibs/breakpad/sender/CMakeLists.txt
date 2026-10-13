# bpreport, the crash report sender of breakpad's dumps (its dialog on the system's FLTK: Linux; jam took FLTK for
# Windows and macOS from Gaijin's devtools)
dagor_add_target(NAME bpreport EXECUTABLE APPLICATION NO_CONFIG_POSTFIX
  FILES_CMAKE sender_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/breakpad ${DAGOR_PROG_DIR}/3rdPartyLibs/libcurl/include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zlib-ng ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/libzip/lib
    ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include
  COMPILE_DEFINITIONS PRIVATE __B_NO_MEM_BASE_INCLUDE CURL_STATICLIB _HAS_EXCEPTIONS=0 ZIP_EXTERN=
  BUILD_DEPENDENCIES PRIVATE
    3rdPartyLibs.libcurl 3rdPartyLibs.arc.libzip 3rdPartyLibs.arc.zlib-ng engine.osApiWrappers engine.memory.minrtl
    engine.perfMon.daProfilerStub engine.perfMon.perfTimerStub 3rdPartyLibs.openssl-3.x System::fltk System::X11
)
