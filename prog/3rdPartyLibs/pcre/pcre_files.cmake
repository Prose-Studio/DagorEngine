if(WIN32)
  set(FILES win32/pcre_chartables.c)
elseif(ANDROID)
  set(FILES linux32/pcre_chartables.c)
elseif(LINUX)
  set(FILES linux64/pcre_chartables.c)
elseif(APPLE)
  set(FILES macosx/pcre_chartables.c)
endif()
list(APPEND FILES
  pcre/pcre_byte_order.c
  pcre/pcre_compile.c
  pcre/pcre_config.c
  pcre/pcre_dfa_exec.c
  pcre/pcre_exec.c
  pcre/pcre_fullinfo.c
  pcre/pcre_get.c
  pcre/pcre_globals.c
  pcre/pcre_jit_compile.c
  pcre/pcre_maketables.c
  pcre/pcre_newline.c
  pcre/pcre_ord2utf8.c
  pcre/pcre_printint.c
  pcre/pcre_refcount.c
  pcre/pcre_string_utils.c
  pcre/pcre_study.c
  pcre/pcre_tables.c
  pcre/pcre_ucd.c
  pcre/pcre_valid_utf8.c
  pcre/pcre_version.c
  pcre/pcre_xclass.c
  pcre/pcrecpp.cc
  pcre/pcre_scanner.cc
  pcre/pcre_stringpiece.cc
  pcre/pcrecpp_nostl.cc
)
