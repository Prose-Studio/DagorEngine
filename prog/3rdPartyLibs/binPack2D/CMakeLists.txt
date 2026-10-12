# 2D rectangle bin packing (Guillotine, MaxRects, Skyline, PowerOfTwo), e.g. for texture atlases
set(includes include)
set(sources src/GuillotineBinPack.cpp src/MaxRectsBinPack.cpp src/SkylineBinPack.cpp src/PowerOfTwoBinPack.cpp)
list(APPEND deps 3rdPartyLibs.eastl)
if(LINUX)
  list(APPEND options -Wno-unused-parameter)
endif()

dagor_add_library(3rdPartyLibs.binPack2D LAX ${sources})
target_include_directories(3rdPartyLibs.binPack2D PRIVATE ${includes})
target_compile_options(3rdPartyLibs.binPack2D PRIVATE ${options})
target_link_libraries(3rdPartyLibs.binPack2D PRIVATE ${deps})
