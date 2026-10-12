# OpenSSL 3 libcrypto (without SHA, which is crypto/sha)
include(../openssl.cmake)
set(c_options ${OPENSSL_C_OPTIONS})
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  # false positive of gcc 13: "rsaz_exp_x2.c:496:16: error: iteration 19 invokes undefined behavior"
  list(APPEND c_options -Wno-aggressive-loop-optimizations -Wno-discarded-qualifiers)
  if(DAGOR_SANITIZE STREQUAL "thread")
    list(APPEND c_options -fno-sanitize=thread)
  endif()
elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND c_options -Wno-incompatible-pointer-types-discards-qualifiers)
  if(DAGOR_SANITIZE STREQUAL "undefined")
    list(APPEND c_options -fno-sanitize=undefined)
  endif()
endif()
if(DAGOR_ARCH STREQUAL "e2k")
  list(APPEND c_options -Wno-reduced-alignment)
endif()

dagor_add_target(NAME 3rdPartyLibs.openssl-3.x.crypto STATIC LAX
  FILES_CMAKE crypto_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${OPENSSL_INCLUDES}
  COMPILE_DEFINITIONS PRIVATE ${OPENSSL_C_DEFINES}
  COMPILE_OPTIONS PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.openssl-3.x.crypto.sha
  LICENSES ${OPENSSL_DIR}/LICENSE.txt
)
