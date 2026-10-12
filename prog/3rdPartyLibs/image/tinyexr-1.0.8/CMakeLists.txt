set(includes ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zlib-ng)
set(sources tinyexr.cc)

dagor_add_library(3rdPartyLibs.image.tinyexr-1.0.8 LAX ${sources})
target_include_directories(3rdPartyLibs.image.tinyexr-1.0.8 PRIVATE ${includes})
