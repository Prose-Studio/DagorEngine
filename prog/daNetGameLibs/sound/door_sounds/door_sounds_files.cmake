set(AllSrcFolder_DAS )
if(DAGOR_GAME_SOUND)
  list(APPEND AllSrcFolder_DAS es)
endif()

dagor_glob_sources(DAS_FILES DIRS ${AllSrcFolder_DAS} GLOB *.das)
