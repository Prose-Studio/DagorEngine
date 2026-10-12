# LZ4 1.9.4 block compression, fast and high compression (lz4, lz4hc)
dagor_add_target(NAME 3rdPartyLibs.arc.lz4 STATIC LAX
  FILES_CMAKE lz4_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
)
