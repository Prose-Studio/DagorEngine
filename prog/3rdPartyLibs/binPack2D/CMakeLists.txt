# 2D rectangle bin packing (Guillotine, MaxRects, Skyline, PowerOfTwo), e.g. for texture atlases
if(LINUX)
  list(APPEND options -Wno-unused-parameter)
endif()

dagor_add_target(NAME 3rdPartyLibs.binPack2D STATIC LAX
  FILES_CMAKE binPack2D_files.cmake
  INCLUDE_DIRECTORIES PRIVATE include
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
)
