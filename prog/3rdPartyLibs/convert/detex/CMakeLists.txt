# detex: BCn/ETC texture decompression
set(sources
  bits.c
  bptc-tables.c
  clamp.c
  convert.c
  dds.c
  decompress-bc.c
  decompress-bptc-float.c
  decompress-bptc.c
  decompress-eac.c
  decompress-etc.c
  decompress-rgtc.c
  division-tables.c
  ktx.c
  raw.c
  texture.c
)
if(CMAKE_CXX_COMPILER_ID MATCHES "^(Clang|AppleClang|GNU)$")
  list(APPEND c_options -Wno-unused-parameter)
endif()

dagor_add_library(3rdPartyLibs.convert.detex LAX ${sources})
target_compile_options(3rdPartyLibs.convert.detex PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>")
