set(AllSrcFolder_DAS main)
set(AllSrcFolder_CPP .)
set(AllSrcFolder_ES .)

dagor_glob_sources(FILES DIRS ${AllSrcFolder_CPP} GLOB *.cpp)
dagor_glob_sources(ES_FILES DIRS ${AllSrcFolder_ES} GLOB *ES.cpp.inl)
dagor_glob_sources(DAS_FILES DIRS ${AllSrcFolder_DAS} GLOB *.das)
