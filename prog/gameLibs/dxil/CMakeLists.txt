# DXIL shader compilation through DXC (dxcompiler loaded at run time) and compiled shader header generation
dagor_add_target(NAME gameLibs.dxil STATIC LAX
  FILES_CMAKE dxil_files.cmake
)
