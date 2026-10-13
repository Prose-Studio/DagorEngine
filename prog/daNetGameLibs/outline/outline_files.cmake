set(AllSrcFolder_ES )
if(DAGOR_GAME_RENDERER)
  list(APPEND AllSrcFolder_ES render)
  set(AllSrcFolder_CPP render/dasModules)
endif()

dagor_glob_sources(FILES DIRS ${AllSrcFolder_CPP} GLOB *.cpp)
dagor_glob_sources(ES_FILES DIRS ${AllSrcFolder_ES} GLOB *ES.cpp.inl)
