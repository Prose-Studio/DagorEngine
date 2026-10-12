# POSIX functions missing on Windows (inet_ntop, inet_pton)
dagor_add_library(3rdPartyLibs.posix LAX src/inet_ntop.c src/inet_pton.c)
dagor_target_force_include(3rdPartyLibs.posix supp/dag_null.h)
