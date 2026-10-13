dagor_add_target(NAME gameLibs.nvCacheTracker STATIC
  FILES_CMAKE nvCacheTracker_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/minhook/Include
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.minhook gameLibs.statsd
)
