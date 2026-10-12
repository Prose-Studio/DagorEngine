# libcurl (HTTP and WebSockets) on the vendored OpenSSL 3, zlib-ng, zstd and brotli
set(includes
  lib
  include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zlib-ng
  ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5
  ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/brotli/include
)
list(APPEND deps 3rdPartyLibs.arc.zlib-ng 3rdPartyLibs.arc.zstd-1.4.5 3rdPartyLibs.arc.brotli)
if(WIN32)
  list(APPEND libs System::ws2_32 System::crypt32 System::bcrypt)
endif()
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND options -Wno-deprecated-declarations)
  list(APPEND libs "$<LINK_LIBRARY:FRAMEWORK,SystemConfiguration>")
endif()
list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include)
list(APPEND deps 3rdPartyLibs.openssl-3.x)
set(c_options
  -DCURL_STATICLIB
  -DBUILDING_LIBCURL
  -DHAVE_BROTLI
  -DHAVE_ZSTD
  -DHAVE_LIBZ
  -DCURL_DISABLE_HTTPSIG # no libjose here, and config-win32.h has no slot to say so
  # the protocols one by one: HTTP_ONLY would switch WebSockets off as well
  -DCURL_DISABLE_DICT
  -DCURL_DISABLE_FILE
  -DCURL_DISABLE_FTP
  -DCURL_DISABLE_GOPHER
  -DCURL_DISABLE_IMAP
  -DCURL_DISABLE_LDAP
  -DCURL_DISABLE_MQTT
  -DCURL_DISABLE_POP3
  -DCURL_DISABLE_RTSP
  -DCURL_DISABLE_SMTP
  -DCURL_DISABLE_TELNET
  -DCURL_DISABLE_TFTP
)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  if(DAGOR_SANITIZE STREQUAL "undefined")
    list(APPEND c_options -fno-sanitize=undefined)
  endif()
  list(APPEND c_options -Wno-incompatible-pointer-types-discards-qualifiers)
endif()
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  list(APPEND c_options -Wno-discarded-qualifiers)
endif()
if(CMAKE_SYSTEM_NAME MATCHES "^(Android|Darwin|Linux|iOS|tvOS)$")
  list(APPEND defines HAVE_CONFIG_H)
endif()

dagor_add_target(NAME 3rdPartyLibs.libcurl STATIC LAX
  FILES_CMAKE libcurl_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE ${defines}
  COMPILE_OPTIONS PRIVATE ${options} "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
  BUILD_DEPENDENCIES
    PUBLIC ${libs}
    PRIVATE ${deps}
)
