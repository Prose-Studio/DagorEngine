set(c_options -DXXH_CPU_LITTLE_ENDIAN)

dagor_add_target(NAME 3rdPartyLibs.arc.zstd-1.5.7 STATIC LAX
  FILES_CMAKE zstd-1.5.7_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR} common compress decompress dictBuilder legacy
  COMPILE_OPTIONS PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
)
