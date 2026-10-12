# libtiff 4.4.0: TIFF image reading and writing (JPEG through jpeg-6b, deflate through zlib-ng)
set(sources
  tif_aux.c
  tif_close.c
  tif_codec.c
  tif_color.c
  tif_compress.c
  tif_dir.c
  tif_dirinfo.c
  tif_dirread.c
  tif_dirwrite.c
  tif_dumpmode.c
  tif_error.c
  tif_extension.c
  tif_fax3.c
  tif_fax3sm.c
  tif_flush.c
  tif_getimage.c
  tif_jbig.c
  tif_jpeg.c
  tif_jpeg_12.c
  tif_lerc.c
  tif_luv.c
  tif_lzma.c
  tif_lzw.c
  tif_next.c
  tif_ojpeg.c
  tif_open.c
  tif_packbits.c
  tif_pixarlog.c
  tif_predict.c
  tif_print.c
  tif_read.c
  tif_strip.c
  tif_swab.c
  tif_thunder.c
  tif_tile.c
  tif_version.c
  tif_warning.c
  tif_webp.c
  tif_write.c
  tif_zip.c
  tif_zstd.c
  tif_stream.cxx
)
if(WIN32)
  list(APPEND sources tif_win32.c)
endif()
if(CMAKE_SYSTEM_NAME MATCHES "^(Darwin|Linux)$")
  list(APPEND sources tif_unix.c)
endif()
set(includes
  ${DAGOR_PROG_DIR}/3rdPartyLibs/image/tiff-4.4.0
  ${DAGOR_PROG_DIR}/3rdPartyLibs/image/jpeg-6b
  ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zlib-ng
)
set(deps 3rdPartyLibs.image.jpeg-6b 3rdPartyLibs.arc.zlib-ng)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND c_options -Wno-format-extra-args)
endif()
if(NOT CMAKE_SYSTEM_NAME MATCHES "^(Android|Darwin|Linux|Windows)$")
  if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    list(APPEND c_options -include stdlib_stub.h)
  endif()
endif()

dagor_add_library(3rdPartyLibs.image.tiff-4.4.0 LAX ${sources})
target_include_directories(3rdPartyLibs.image.tiff-4.4.0 PRIVATE ${includes})
target_compile_options(3rdPartyLibs.image.tiff-4.4.0 PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>")
target_link_libraries(3rdPartyLibs.image.tiff-4.4.0 PRIVATE ${deps})
