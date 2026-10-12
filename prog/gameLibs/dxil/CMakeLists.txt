# DXIL shader compilation through DXC (dxcompiler loaded at run time) and compiled shader header generation
dagor_add_target(NAME gameLibs.dxil STATIC LAX
  FILES_CMAKE dxil_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/dagorInclude
)
