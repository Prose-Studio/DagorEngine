list(APPEND c_options -DHAVE_CONFIG_H -DFLOAT_APPROX)
if(LINUX)
  list(APPEND c_options -Wno-unused-result)
endif()

dagor_add_target(NAME 3rdPartyLibs.codecs.rnnoise STATIC LAX
  FILES_CMAKE rnnoise_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR} include src
  COMPILE_OPTIONS PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
)
