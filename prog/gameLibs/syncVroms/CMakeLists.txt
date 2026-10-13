# the vroms' hashes: BLAKE3, shortened (vromHash_sha1.cpp is the other algorithm, which no game uses)
dagor_add_target(NAME gameLibs.syncVroms STATIC
  FILES_CMAKE syncVroms_files.cmake
  BUILD_DEPENDENCIES PRIVATE gameLibs.compressionUtils 3rdPartyLibs.hash 3rdPartyLibs.hash.BLAKE3
)
