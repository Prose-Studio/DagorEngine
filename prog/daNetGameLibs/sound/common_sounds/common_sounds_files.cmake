set(AllSrcFolder_DAS )
if(DAGOR_GAME_SOUND)
  set(AllSrcFolder_ES .)
  list(APPEND AllSrcFolder_DAS modules es)
endif()

dagor_glob_sources(ES_FILES DIRS ${AllSrcFolder_ES} GLOB *ES.cpp.inl)
dagor_glob_sources(DAS_FILES DIRS ${AllSrcFolder_DAS} GLOB *.das)
