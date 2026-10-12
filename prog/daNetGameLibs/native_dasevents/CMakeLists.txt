dagor_add_dng_module(daNetGameLibs.native_dasevents DAS DAS_DIRS main ui)
target_include_directories(daNetGameLibs.native_dasevents PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include)
target_link_libraries(daNetGameLibs.native_dasevents PRIVATE Dagor::Phys)
