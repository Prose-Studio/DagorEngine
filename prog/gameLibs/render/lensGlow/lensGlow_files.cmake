set(AllSrcFolder_CPP )
if(DAGOR_GAME_RENDERER)
  list(APPEND AllSrcFolder_CPP render)
endif()

dagor_glob_sources(FILES DIRS ${AllSrcFolder_CPP} GLOB *.cpp)
