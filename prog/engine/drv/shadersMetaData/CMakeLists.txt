# Shader metadata shared by the drivers and the shader compilers
add_subdirectory(dx11)
add_subdirectory(dxil)
add_subdirectory(spirv)

set(sources shaderSource.cpp)

dagor_add_library(engine.drv.shadersMetaData LAX ${sources})
