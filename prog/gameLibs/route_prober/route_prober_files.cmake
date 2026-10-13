set(AllSrcFolder_DAS )
if(NOT DAGOR_DEDICATED)
  list(APPEND AllSrcFolder_DAS main)
endif()

dagor_glob_sources(DAS_FILES DIRS ${AllSrcFolder_DAS} GLOB *.das)
