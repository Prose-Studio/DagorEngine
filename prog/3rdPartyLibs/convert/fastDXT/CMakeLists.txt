# Fast DXT (BC1-3) compressors
set(sources fastDXT.cpp rygDXT.cpp)
if(DAGOR_ARCH MATCHES "^(e2k|x86_64)$")
  list(APPEND defines DXT_INTR)
endif()
set(includes ${DAGOR_PROG_DIR}/3rdPartyLibs/convert/fastDXT)

dagor_add_library(3rdPartyLibs.convert.fastDXT LAX ${sources})
target_include_directories(3rdPartyLibs.convert.fastDXT PRIVATE ${includes})
target_compile_definitions(3rdPartyLibs.convert.fastDXT PRIVATE ${defines})
