# the sources of libcrypto (openssl_collect_c and _asm: openssl.cmake)
foreach(file asn1_dsa bsearch context core_algorithm core_fetch core_namemap cpt_err cversion der_writer ebcdic ex_data
             info init initthread mem mem_sec o_dir o_fopen o_init o_str o_time packet param_build param_build_set params
             params_dup params_from_text passphrase provider provider_child provider_conf provider_core
             provider_predefined punycode self_test_core sparse_array trace uid dso/dso_openssl dso/dso_lib dso/dso_err
             dso/dso_dl poly1305/poly1305)
  list(APPEND FILES ${OPENSSL_DIR}/crypto/${file}.c)
endforeach()
set(ec_int128 ecp_nistp224.c ecp_nistp256.c ecp_nistp521.c)
openssl_collect_c(FILES crypto/aes aes_core.c aes_cbc.c)
foreach(dir aria asn1 async bf bio blake2 buffer cast cmac cmp cms comp conf crmf ct dh dsa ec/curve448
            ec/curve448/arch_32 ec/curve448/arch_64 encode_decode err ess evp ffc hmac http idea kdf lhash md4 md5 mdc2
            modes objects ocsp pem pkcs12 pkcs7 property rand rc2 rc5 ripemd rsa seed siphash sm2 sm3 sm4 srp stack
            store ts txt_db ui x509 x509v3)
  openssl_collect_c(FILES crypto/${dir})
endforeach()
openssl_collect_c(FILES crypto/bn bn_sparc.c)
openssl_collect_c(FILES crypto/camellia camellia.c cmll_cbc.c)
openssl_collect_c(FILES crypto/des ncbc_enc.c)
openssl_collect_c(FILES crypto/ec ${ec_int128} ecp_nistz256_table.c)
openssl_collect_c(FILES crypto/rc4 rc4_enc.c rc4_skey.c)
openssl_collect_c(FILES crypto/whrlpool wp_block.c)

if(OPENSSL_ASM)
  foreach(dir aes bn camellia chacha ec md5 modes poly1305 rc4 whrlpool)
    openssl_collect_asm(FILES crypto/${dir})
  endforeach()
else()
  foreach(file aes/aes_core aes/aes_cbc chacha/chacha_enc mem_clr whrlpool/wp_block camellia/camellia camellia/cmll_cbc
               rc4/rc4_enc rc4/rc4_skey)
    list(APPEND FILES ${OPENSSL_DIR}/crypto/${file}.c)
  endforeach()
endif()
if(WIN32)
  list(APPEND FILES ${OPENSSL_DIR}/crypto/threads_win.c ${OPENSSL_DIR}/crypto/async/arch/async_win.c)
else()
  if(CMAKE_SYSTEM_NAME MATCHES "^(Android|iOS)$")
    list(APPEND FILES ${OPENSSL_DIR}/crypto/async/arch/async_null.c)
  else()
    list(APPEND FILES ${OPENSSL_DIR}/crypto/async/arch/async_posix.c)
  endif()
  list(APPEND FILES ${OPENSSL_DIR}/crypto/threads_pthread.c)
  list(TRANSFORM ec_int128 PREPEND "${OPENSSL_DIR}/crypto/ec/")
  list(APPEND FILES ${ec_int128})
endif()
if(DAGOR_ARCH STREQUAL "e2k")
  set_property(SOURCE ${OPENSSL_DIR}/crypto/async/arch/async_posix.c APPEND PROPERTY COMPILE_OPTIONS -Dmakecontext=makecontext_e2k)
endif()
