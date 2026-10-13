if(DAGOR_GAME_RENDERER)
  dagor_glob_sources(ES_FILES DIRS render GLOB *ES.cpp.inl)
  # the debug window in Dev and Dbg
  dagor_glob_sources(debug DIRS debug GLOB *ES.cpp.inl)
  list(TRANSFORM debug REPLACE "^(.+)$" "$<$<CONFIG:Dev,Dbg>:\\1>")
  list(APPEND ES_FILES ${debug})
endif()
