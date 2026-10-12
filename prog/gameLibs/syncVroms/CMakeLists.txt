# the vroms' hashes: BLAKE3, shortened (vromHash_sha1.cpp is the other algorithm, which no game uses)
dagor_add_library(gameLibs.syncVroms vromHash.cpp syncVroms.cpp vromHash_blake3short.cpp)
target_include_directories(gameLibs.syncVroms PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
target_link_libraries(gameLibs.syncVroms PRIVATE gameLibs.compressionUtils 3rdPartyLibs.hash 3rdPartyLibs.hash.BLAKE3)
