# the sources of libssl and the default provider (openssl_collect_c: openssl.cmake)
openssl_collect_c(FILES providers/common securitycheck_fips.c)
foreach(dir providers/common/der providers/implementations/asymciphers providers/implementations/digests
            providers/implementations/encode_decode providers/implementations/exchange providers/implementations/kdfs
            providers/implementations/kem providers/implementations/keymgmt providers/implementations/rands
            providers/implementations/signature providers/implementations/storemgmt ssl ssl/record ssl/statem)
  openssl_collect_c(FILES ${dir})
endforeach()
openssl_collect_c(FILES providers/implementations/ciphers cipher_rc4_hmac_md5_hw.c)
openssl_collect_c(FILES providers/implementations/macs blake2_mac_impl.c)
list(APPEND sources providers/baseprov.c providers/defltprov.c providers/nullprov.c providers/prov_running.c
  gaijin_stubs/getenv.c)
if(WIN32)
  list(APPEND sources providers/implementations/rands/seeding/rand_win.c)
else()
  list(APPEND sources providers/implementations/rands/seeding/rand_unix.c)
endif()
