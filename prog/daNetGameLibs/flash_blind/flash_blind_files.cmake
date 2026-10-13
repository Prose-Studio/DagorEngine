set(AllSrcFolder_ES )
set(AllSrcFolder_DAS )
if(DAGOR_GAME_RENDERER)
  list(APPEND AllSrcFolder_ES render)
  list(APPEND AllSrcFolder_DAS render)
endif()

dagor_glob_sources(ES_FILES DIRS ${AllSrcFolder_ES} GLOB *ES.cpp.inl)
dagor_glob_sources(DAS_FILES DIRS ${AllSrcFolder_DAS} GLOB *.das)
