# encoder, jam's IncludeEncoder)
if(WIN32)
  list(APPEND c_options /wd4554)
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND c_options -Wno-logical-op-parentheses -Wno-parentheses -Wno-tautological-compare)
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES "^(Clang|AppleClang|GNU)$")
  list(APPEND options -Wno-unused-parameter)
endif()

dagor_add_target(NAME 3rdPartyLibs.codecs.libtheora-1.0 STATIC LAX
  FILES_CMAKE libtheora-1.0_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ../include
  COMPILE_OPTIONS PRIVATE ${options} "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
)
