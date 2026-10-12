# Zstandard 1.4.5 with legacy format support
set(includes
  ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5
  ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5/common
  ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5/compress
  ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5/decompress
  ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5/dictBuilder
  ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5/legacy
)
set(AllSrcFolder_C common compress decompress dictBuilder legacy src/builtin src/simulate src/misc)
dagor_glob_sources(sources DIRS ${AllSrcFolder_C} GLOB *.c)
set(c_options -DZSTD_LEGACY_SUPPORT -DXXH_CPU_LITTLE_ENDIAN)

dagor_add_library(3rdPartyLibs.arc.zstd-1.4.5 LAX ${sources})
target_include_directories(3rdPartyLibs.arc.zstd-1.4.5 PRIVATE ${includes})
target_compile_options(3rdPartyLibs.arc.zstd-1.4.5 PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>")
