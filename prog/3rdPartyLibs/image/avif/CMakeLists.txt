# libavif 0.11.1: the AV1 Image File Format, with dav1d as its only codec (decoding)
set(includes ${DAGOR_PROG_DIR}/3rdPartyLibs/image/avif)
set(includes include ${DAGOR_PROG_DIR}/3rdPartyLibs/codecs/dav1d/include)

dagor_add_target(NAME 3rdPartyLibs.image.avif STATIC LAX
  FILES_CMAKE avif_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE AVIF_CODEC_DAV1D
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.codecs.dav1d
)
