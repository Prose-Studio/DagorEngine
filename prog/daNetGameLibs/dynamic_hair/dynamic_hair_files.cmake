set(AllSrcFolder_ES )
if(DAGOR_GAME_RENDERER)
  list(APPEND AllSrcFolder_ES render)
endif()

dagor_glob_sources(ES_FILES DIRS ${AllSrcFolder_ES} GLOB *ES.cpp.inl)
