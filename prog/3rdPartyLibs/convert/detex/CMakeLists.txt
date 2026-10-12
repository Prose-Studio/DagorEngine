# detex: BCn/ETC texture decompression
if(CMAKE_CXX_COMPILER_ID MATCHES "^(Clang|AppleClang|GNU)$")
  list(APPEND c_options -Wno-unused-parameter)
endif()

dagor_add_target(NAME 3rdPartyLibs.convert.detex STATIC LAX
  FILES_CMAKE detex_files.cmake
  COMPILE_OPTIONS PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
)
