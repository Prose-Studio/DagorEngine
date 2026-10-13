dagor_add_target(NAME gameLibs.contentUpdater.utils STATIC
  FILES_CMAKE utils_files.cmake
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)
# the updater's version numbers have one digit after the dot
set(gen "${CMAKE_CURRENT_BINARY_DIR}/gen")
file(CONFIGURE OUTPUT "${gen}/minorVersionDigitsCount.cpp"
  CONTENT "int get_updater_minor_version_digits_count() { return 1; }\n")
target_sources(gameLibs.contentUpdater.utils PRIVATE "${gen}/minorVersionDigitsCount.cpp")
