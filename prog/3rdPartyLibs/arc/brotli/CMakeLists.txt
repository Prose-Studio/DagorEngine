# Brotli compression
dagor_add_target(NAME 3rdPartyLibs.arc.brotli STATIC LAX
  FILES_CMAKE brotli_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/brotli/common ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/brotli/include
)
