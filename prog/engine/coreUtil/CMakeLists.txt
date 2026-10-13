# Core utilities: simple parameter blocks, base64, localization tables, fly mode
dagor_add_target(NAME engine.coreUtil STATIC
  FILES_CMAKE coreUtil_files.cmake
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
)
