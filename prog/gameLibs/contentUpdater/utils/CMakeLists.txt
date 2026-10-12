# the updater's version numbers have one digit after the dot
set(gen "${CMAKE_CURRENT_BINARY_DIR}/gen")
file(CONFIGURE OUTPUT "${gen}/minorVersionDigitsCount.cpp"
  CONTENT "int get_updater_minor_version_digits_count() { return 1; }\n")

dagor_add_library(gameLibs.contentUpdater.utils pathUtils.cpp version.cpp "${gen}/minorVersionDigitsCount.cpp")
target_include_directories(gameLibs.contentUpdater.utils PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
target_link_libraries(gameLibs.contentUpdater.utils PRIVATE Dagor::Quirrel)
