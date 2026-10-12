# IJG libjpeg 6b
set(includes ${DAGOR_PROG_DIR}/3rdPartyLibs/image/jpeg-6b)
set(sources
  jcapimin.c
  jcapistd.c
  jccoefct.c
  jccolor.c
  jcdctmgr.c
  jchuff.c
  jcinit.c
  jcmainct.c
  jcmarker.c
  jcmaster.c
  jcomapi.c
  jcparam.c
  jcphuff.c
  jcprepct.c
  jcsample.c
  jctrans.c
  jdapimin.c
  jdapistd.c
  jdatadst.c
  jdatasrc.c
  jdcoefct.c
  jdcolor.c
  jddctmgr.c
  jdhuff.c
  jdinput.c
  jdmainct.c
  jdmarker.c
  jdmaster.c
  jdmerge.c
  jdphuff.c
  jdpostct.c
  jdsample.c
  jdtrans.c
  jerror.c
  jfdctflt.c
  jfdctfst.c
  jfdctint.c
  jidctflt.c
  jidctfst.c
  jidctint.c
  jidctred.c
  jquant1.c
  jquant2.c
  jutils.c
  jmemmgr.c
  jmemdagor.c
)
set(defines NO_GETENV)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND options -Wno-shift-negative-value)
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES "^(Clang|AppleClang|GNU)$")
  list(APPEND options -Wno-unused-parameter)
endif()
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND options -Wno-deprecated-declarations -Wno-shift-negative-value)
endif()

dagor_add_library(3rdPartyLibs.image.jpeg-6b LAX ${sources})
target_include_directories(3rdPartyLibs.image.jpeg-6b PRIVATE ${includes})
target_compile_definitions(3rdPartyLibs.image.jpeg-6b PRIVATE ${defines})
target_compile_options(3rdPartyLibs.image.jpeg-6b PRIVATE ${options})
