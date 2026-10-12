# Zstandard 1.4.5 with legacy format support
set(c_options -DZSTD_LEGACY_SUPPORT -DXXH_CPU_LITTLE_ENDIAN)

dagor_add_target(NAME 3rdPartyLibs.arc.zstd-1.4.5 STATIC LAX
  FILES_CMAKE zstd-1.4.5_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5 ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5/common
    ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5/compress ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5/decompress
    ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5/dictBuilder ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5/legacy
  COMPILE_OPTIONS PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
)
