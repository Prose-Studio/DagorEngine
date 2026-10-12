# LZMA SDK 9.20 encoder and decoder
set(sources LzmaDec.c LzmaEnc.c LzFind.c)
set(c_options -D_7ZIP_ST -D__B_KERNEL_LIB)

dagor_add_library(3rdPartyLibs.arc.lzma-9.20 LAX ${sources})
target_compile_options(3rdPartyLibs.arc.lzma-9.20 PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>")
