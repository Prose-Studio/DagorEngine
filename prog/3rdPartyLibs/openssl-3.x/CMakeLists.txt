# OpenSSL 3: libssl and the default provider, on libcrypto (crypto/), with zlib compression
include(openssl.cmake)
set(c_options ${OPENSSL_C_OPTIONS})
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang" AND DAGOR_SANITIZE STREQUAL "undefined")
  list(APPEND c_options -fno-sanitize=undefined)
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "GNU" AND DAGOR_SANITIZE STREQUAL "thread")
  list(APPEND c_options -fno-sanitize=thread)
endif()
set(libs)
if(WIN32)
  set(libs System::ws2_32 System::advapi32)
endif()

dagor_add_target(NAME 3rdPartyLibs.openssl-3.x STATIC LAX
  FILES_CMAKE openssl-3.x_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${OPENSSL_INCLUDES}
  COMPILE_DEFINITIONS PRIVATE ${OPENSSL_C_DEFINES} ZLIB
  COMPILE_OPTIONS PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
  BUILD_DEPENDENCIES
    PUBLIC ${libs}
    PRIVATE 3rdPartyLibs.openssl-3.x.crypto 3rdPartyLibs.arc.zlib-ng
  LICENSES LICENSE.txt
)
