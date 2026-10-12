# OpenSSL 3: libssl and the default provider, on libcrypto (crypto/), with zlib compression
add_subdirectory(crypto)

include(openssl.cmake)

set(sources)
openssl_collect_c(sources providers/common securitycheck_fips.c)
foreach(dir providers/common/der providers/implementations/asymciphers providers/implementations/digests
            providers/implementations/encode_decode providers/implementations/exchange providers/implementations/kdfs
            providers/implementations/kem providers/implementations/keymgmt providers/implementations/rands
            providers/implementations/signature providers/implementations/storemgmt ssl ssl/record ssl/statem)
  openssl_collect_c(sources ${dir})
endforeach()
openssl_collect_c(sources providers/implementations/ciphers cipher_rc4_hmac_md5_hw.c)
openssl_collect_c(sources providers/implementations/macs blake2_mac_impl.c)
list(APPEND sources providers/baseprov.c providers/defltprov.c providers/nullprov.c providers/prov_running.c
  gaijin_stubs/getenv.c)
if(WIN32)
  list(APPEND sources providers/implementations/rands/seeding/rand_win.c)
else()
  list(APPEND sources providers/implementations/rands/seeding/rand_unix.c)
endif()

set(c_options ${OPENSSL_C_OPTIONS})
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang" AND DAGOR_SANITIZE STREQUAL "undefined")
  list(APPEND c_options -fno-sanitize=undefined)
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "GNU" AND DAGOR_SANITIZE STREQUAL "thread")
  list(APPEND c_options -fno-sanitize=thread)
endif()
set(libs)
if(WIN32)
  set(libs System::ws2_32 System::advapi32)
elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  set_property(SOURCE ssl/ssl_lib.c APPEND PROPERTY COMPILE_OPTIONS -Wno-deprecated-declarations)
endif()

dagor_add_library(3rdPartyLibs.openssl-3.x LAX ${sources})
target_include_directories(3rdPartyLibs.openssl-3.x PRIVATE ${OPENSSL_INCLUDES})
target_compile_definitions(3rdPartyLibs.openssl-3.x PRIVATE ${OPENSSL_C_DEFINES} ZLIB)
target_compile_options(3rdPartyLibs.openssl-3.x PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>")
target_link_libraries(3rdPartyLibs.openssl-3.x PRIVATE 3rdPartyLibs.openssl-3.x.crypto 3rdPartyLibs.arc.zlib-ng)
target_link_libraries(3rdPartyLibs.openssl-3.x PUBLIC ${libs})
dagor_target_licenses(3rdPartyLibs.openssl-3.x LICENSE.txt)
