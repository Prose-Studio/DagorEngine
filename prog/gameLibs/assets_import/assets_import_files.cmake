# the in-game asset manager is not ported (CMakeLists.txt): its stub
if(DAGOR_GAME_RENDERER)
  dagor_glob_sources(ES_FILES DIRS stub GLOB *ES.cpp.inl)
endif()
