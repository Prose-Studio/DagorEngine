# outside Rel
if(DAGOR_GAME_RENDERER)
  dagor_glob_sources(ES_FILES DIRS render GLOB *ES.cpp.inl)
  list(TRANSFORM ES_FILES REPLACE "^(.+)$" "$<$<NOT:$<CONFIG:Rel>>:\\1>")
endif()
