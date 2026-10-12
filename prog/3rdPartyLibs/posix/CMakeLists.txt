# POSIX functions missing on Windows (inet_ntop, inet_pton)
if(WIN32)
  set(sources src/inet_ntop.c src/inet_pton.c)
endif()
list(APPEND force_includes supp/dag_null.h)

dagor_add_library(3rdPartyLibs.posix LAX ${sources})
dagor_target_force_include(3rdPartyLibs.posix ${force_includes})
