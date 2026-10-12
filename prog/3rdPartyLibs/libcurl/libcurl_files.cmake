# the backends compile to nothing unless their USE_* macro is on, so the whole tree is taken
dagor_glob_sources(FILES DIRS lib lib/curlx lib/vauth lib/vdns lib/vquic lib/vssh lib/vtls GLOB *.c)
