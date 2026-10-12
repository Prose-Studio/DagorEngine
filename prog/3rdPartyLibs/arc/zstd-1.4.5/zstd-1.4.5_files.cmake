set(AllSrcFolder_C common compress decompress dictBuilder legacy src/builtin src/simulate src/misc)
dagor_glob_sources(FILES DIRS ${AllSrcFolder_C} GLOB *.c)
