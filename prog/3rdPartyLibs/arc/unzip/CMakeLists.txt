if(NOT CMAKE_SYSTEM_NAME MATCHES "^(Android|Linux|Darwin|Windows)$")
  list(APPEND c_options -Dftello=ftell -Dfseeko=fseek)
endif()

dagor_add_target(NAME 3rdPartyLibs.arc.unzip STATIC LAX
  FILES_CMAKE unzip_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zlib-ng
  COMPILE_OPTIONS PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
)
