set(AllSrcFolder_ES )
set(AllSrcFolder_CPP )
set(AllSrcFolder_DAS )
list(APPEND AllSrcFolder_ES es)
list(APPEND AllSrcFolder_CPP animation dasModules)
list(APPEND AllSrcFolder_DAS das)

dagor_glob_sources(FILES DIRS ${AllSrcFolder_CPP} GLOB *.cpp)
dagor_glob_sources(ES_FILES DIRS ${AllSrcFolder_ES} GLOB *ES.cpp.inl)
dagor_glob_sources(DAS_FILES DIRS ${AllSrcFolder_DAS} GLOB *.das)
# the debug entity systems in Dev and Dbg
dagor_glob_sources(debug DIRS debug/es GLOB *ES.cpp.inl)
list(TRANSFORM debug REPLACE "^(.+)$" "$<$<CONFIG:Dev,Dbg>:\\1>")
list(APPEND ES_FILES ${debug})
