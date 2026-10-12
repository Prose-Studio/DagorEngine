# libb64 base64 encoder/decoder
dagor_add_target(NAME 3rdPartyLibs.libb64 STATIC LAX
  FILES_CMAKE libb64_files.cmake
  INCLUDE_DIRECTORIES PRIVATE include
)
