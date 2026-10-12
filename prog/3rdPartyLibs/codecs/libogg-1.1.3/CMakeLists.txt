set(includes ../include)
set(sources src/bitwise.c src/framing.c)

dagor_add_library(3rdPartyLibs.codecs.libogg-1.1.3 LAX ${sources})
target_include_directories(3rdPartyLibs.codecs.libogg-1.1.3 PRIVATE ${includes})
