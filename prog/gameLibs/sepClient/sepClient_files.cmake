set(AllSrcFolder_CPP .)
dagor_glob_sources(FILES DIRS ${AllSrcFolder_CPP} GLOB *.cpp)
list(APPEND FILES asyncHostnameResolver/asyncHostnameResolverCAres.cpp)
