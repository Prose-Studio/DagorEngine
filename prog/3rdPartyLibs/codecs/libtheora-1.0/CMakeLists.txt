# encoder, jam's IncludeEncoder)
set(includes ../include)
set(dec_src
  apiwrapper.c
  bitpack.c
  decapiwrapper.c
  decinfo.c
  decode.c
  dequant.c
  fragment.c
  huffdec.c
  idct.c
  info.c
  internal.c
  quant.c
  state.c
)
list(TRANSFORM dec_src PREPEND lib/dec/)
set(sources ${dec_src} lib/enc/encoder_disabled.c)
if(WIN32)
  list(APPEND c_options /wd4554)
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND c_options -Wno-logical-op-parentheses -Wno-parentheses -Wno-tautological-compare)
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES "^(Clang|AppleClang|GNU)$")
  list(APPEND options -Wno-unused-parameter)
endif()

dagor_add_library(3rdPartyLibs.codecs.libtheora-1.0 LAX ${sources})
target_include_directories(3rdPartyLibs.codecs.libtheora-1.0 PRIVATE ${includes})
target_compile_options(3rdPartyLibs.codecs.libtheora-1.0 PRIVATE ${options})
target_compile_options(3rdPartyLibs.codecs.libtheora-1.0 PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>")
