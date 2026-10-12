if(DAGOR_GAME_RENDERER)
  dagor_glob_sources(FILES DIRS render GLOB *.cpp)
  dagor_glob_sources(ES_FILES DIRS render GLOB *ES.cpp.inl)
endif()
