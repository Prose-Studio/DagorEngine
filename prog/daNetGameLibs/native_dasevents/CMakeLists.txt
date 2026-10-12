dagor_add_dng_module(NAME daNetGameLibs.native_dasevents DAS
  FILES_CMAKE native_dasevents_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  BUILD_DEPENDENCIES PRIVATE Dagor::Phys
)
