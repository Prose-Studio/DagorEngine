# Public domain bencode (the BitTorrent encoding) decoder
set(includes ${CMAKE_CURRENT_SOURCE_DIR})
set(sources bencode.c)
if(WIN32)
  list(APPEND c_options -Dstrtoll=_strtoi64)
endif()

dagor_add_library(3rdPartyLibs.bencode LAX ${sources})
target_include_directories(3rdPartyLibs.bencode PRIVATE ${includes})
target_compile_options(3rdPartyLibs.bencode PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>")
