if(CMAKE_SYSTEM_NAME MATCHES "^(Linux|Darwin|Windows)$")
  list(APPEND defines SQUISH_USE_SSE=2)
endif()

dagor_add_target(NAME 3rdPartyLibs.convert.squish STATIC LAX
  FILES_CMAKE squish_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/convert/squish
  COMPILE_DEFINITIONS PRIVATE ${defines}
)
