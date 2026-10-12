set(includes ${DAGOR_PROG_DIR}/3rdPartyLibs/mongoose)
if(WIN32)
  list(APPEND deps 3rdPartyLibs.posix)
endif()
list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include)
list(APPEND deps 3rdPartyLibs.openssl-3.x)
list(APPEND c_options -DNO_CGI -DNO_SSL_DL -DNO_POPEN -DUSE_WEBSOCKET)
if(WIN32)
  list(APPEND c_options /wd4267)
endif()

dagor_add_target(NAME 3rdPartyLibs.mongoose STATIC LAX
  FILES_CMAKE mongoose_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_OPTIONS PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
