# LZMA SDK 9.20 encoder and decoder
set(c_options -D_7ZIP_ST -D__B_KERNEL_LIB)

dagor_add_target(NAME 3rdPartyLibs.arc.lzma-9.20 STATIC LAX
  FILES_CMAKE lzma-9.20_files.cmake
  COMPILE_OPTIONS PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
)
