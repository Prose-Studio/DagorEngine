set(AllSrcFolder_DAS )
if(DAGOR_GAME_SOUND_NET)
  list(APPEND AllSrcFolder_DAS es modules)
endif()

dagor_glob_sources(DAS_FILES DIRS ${AllSrcFolder_DAS} GLOB *.das)
