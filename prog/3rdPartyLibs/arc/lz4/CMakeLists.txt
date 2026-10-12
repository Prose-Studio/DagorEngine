# LZ4 1.9.4 block compression, fast and high compression (lz4, lz4hc)
set(includes ${CMAKE_CURRENT_SOURCE_DIR})
set(sources lz4.c lz4hc.c)

dagor_add_library(3rdPartyLibs.arc.lz4 LAX ${sources})
target_include_directories(3rdPartyLibs.arc.lz4 PRIVATE ${includes})
