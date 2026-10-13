set(AllSrcFolder_CPP . ./dasModules)
set(AllSrcFolder_ES .)

dagor_glob_sources(FILES DIRS ${AllSrcFolder_CPP} GLOB *.cpp)
dagor_glob_sources(ES_FILES DIRS ${AllSrcFolder_ES} GLOB *ES.cpp.inl)
