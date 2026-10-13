set(AllSrcFolder_CPP )
if(DAGOR_GAME_RENDERER)
  set(AllSrcFolder_CPP ui)
endif()

dagor_glob_sources(FILES DIRS ${AllSrcFolder_CPP} GLOB *.cpp)
