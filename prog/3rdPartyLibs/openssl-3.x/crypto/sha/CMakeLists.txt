# OpenSSL's SHA-1/2/3 alone (with the CPU detection it needs), for the libraries that hash without the rest of OpenSSL
include(../../openssl.cmake)
set(libs)
if(WIN32)
  set(libs System::ws2_32 System::advapi32)
endif()

dagor_add_target(NAME 3rdPartyLibs.openssl-3.x.crypto.sha STATIC LAX
  FILES_CMAKE sha_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${OPENSSL_INCLUDES}
  COMPILE_DEFINITIONS PRIVATE ${OPENSSL_C_DEFINES}
  COMPILE_OPTIONS PRIVATE "$<$<COMPILE_LANGUAGE:C>:${OPENSSL_C_OPTIONS}>"
  BUILD_DEPENDENCIES PUBLIC ${libs}
  LICENSES ${OPENSSL_DIR}/LICENSE.txt
)
