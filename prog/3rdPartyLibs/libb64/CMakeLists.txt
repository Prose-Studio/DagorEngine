# libb64 base64 encoder/decoder
set(includes include)
set(sources src/cdecode.c src/cencode.c)

dagor_add_library(3rdPartyLibs.libb64 LAX ${sources})
target_include_directories(3rdPartyLibs.libb64 PRIVATE ${includes})
