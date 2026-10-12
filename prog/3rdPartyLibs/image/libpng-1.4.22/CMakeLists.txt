# libpng 1.4.22 (on zlib-ng)
set(includes ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zlib-ng)
set(sources
  png.c
  pngerror.c
  pngget.c
  pngmem.c
  pngpread.c
  pngread.c
  pngrio.c
  pngrtran.c
  pngrutil.c
  pngset.c
  pngtrans.c
  pngwio.c
  pngwrite.c
  pngwtran.c
  pngwutil.c
)
set(defines PNG_NO_CONSOLE_IO PNG_NO_WRITE_FLUSH)
if(DAGOR_ARCH STREQUAL "x86_64" AND WIN32)
  list(APPEND c_options /wd4267)
endif()

dagor_add_library(3rdPartyLibs.image.libpng-1.4.22 LAX ${sources})
target_include_directories(3rdPartyLibs.image.libpng-1.4.22 PRIVATE ${includes})
target_compile_definitions(3rdPartyLibs.image.libpng-1.4.22 PRIVATE ${defines})
target_compile_options(3rdPartyLibs.image.libpng-1.4.22 PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>")
