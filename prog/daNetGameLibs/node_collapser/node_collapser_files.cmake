set(AllSrcFolder_DAS )
if(DAGOR_GAME_RENDERER)
  list(APPEND AllSrcFolder_DAS render)
endif()

dagor_glob_sources(DAS_FILES DIRS ${AllSrcFolder_DAS} GLOB *.das)
