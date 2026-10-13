# Image loading/saving (TGA, JPEG, PSD, PNG, AVIF, TIFF, EXR, DDS, SVG), resampling and DXT compression
set(options)
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  list(APPEND options -Wno-uninitialized) # false positives of gcc 11
endif()

dagor_add_target(NAME engine.image STATIC LAX
  FILES_CMAKE image_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zlib-ng
    ${DAGOR_PROG_DIR}/3rdPartyLibs/binPack2D/include ${DAGOR_PROG_DIR}/3rdPartyLibs/image/avif/include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/convert/fastDXT
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE
    3rdPartyLibs.convert.fastDXT 3rdPartyLibs.image.jpeg-6b 3rdPartyLibs.image.libpng-1.4.22
    3rdPartyLibs.image.imageresampler
  LICENSES ${DAGOR_PROG_DIR}/3rdPartyLibs/nanosvg
)
