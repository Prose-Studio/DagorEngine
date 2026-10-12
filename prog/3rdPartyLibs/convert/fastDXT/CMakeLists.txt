# Fast DXT (BC1-3) compressors
if(DAGOR_ARCH MATCHES "^(e2k|x86_64)$")
  list(APPEND defines DXT_INTR)
endif()

dagor_add_target(NAME 3rdPartyLibs.convert.fastDXT STATIC LAX
  FILES_CMAKE fastDXT_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/convert/fastDXT
  COMPILE_DEFINITIONS PRIVATE ${defines}
)
