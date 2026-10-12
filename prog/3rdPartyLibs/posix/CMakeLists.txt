# POSIX functions missing on Windows (inet_ntop, inet_pton)
dagor_add_target(NAME 3rdPartyLibs.posix STATIC LAX
  FILES_CMAKE posix_files.cmake
  FORCE_INCLUDES supp/dag_null.h
)
