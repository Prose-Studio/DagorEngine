# Shader metadata shared by the drivers and the shader compilers
add_subdirectory(dx11)
add_subdirectory(dxil)
add_subdirectory(spirv)

dagor_add_target(NAME engine.drv.shadersMetaData STATIC LAX
  FILES_CMAKE shadersMetaData_files.cmake
)
