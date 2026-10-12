# Public domain bencode (the BitTorrent encoding) decoder
if(WIN32)
  list(APPEND c_options -Dstrtoll=_strtoi64)
endif()

dagor_add_target(NAME 3rdPartyLibs.bencode STATIC LAX
  FILES_CMAKE bencode_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
  COMPILE_OPTIONS PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
)
