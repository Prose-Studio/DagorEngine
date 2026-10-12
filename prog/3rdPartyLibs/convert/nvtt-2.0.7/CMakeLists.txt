# NVIDIA Texture Tools 2.0.7: DXT compression (with squish), image filtering, normal maps and DDS I/O
set(defines NVTT_EXPORTS)
if(DAGOR_ARCH MATCHES "^(e2k|x86_64)$")
  list(APPEND defines __SSE2__ __SSE__ __MMX__)
endif()
if(WIN32)
  list(APPEND defines WIN32 _WINDOWS _USRDLL)
endif()
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND defines SQUISH_USE_ALTIVEC=0)
endif()

dagor_add_target(NAME 3rdPartyLibs.convert.nvtt-2.0.7 STATIC LAX
  FILES_CMAKE nvtt-2.0.7_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/convert/nvtt-2.0.7 ${DAGOR_PROG_DIR}/3rdPartyLibs/image/jpeg-6b
  COMPILE_DEFINITIONS PRIVATE ${defines}
)
