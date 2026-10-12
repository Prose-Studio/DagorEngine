dagor_add_target(NAME 3rdPartyLibs.image.tinyexr-1.0.8 STATIC LAX
  FILES_CMAKE tinyexr-1.0.8_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zlib-ng
)
