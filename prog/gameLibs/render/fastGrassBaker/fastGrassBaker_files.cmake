set(dir ${CMAKE_CURRENT_LIST_DIR})
set(FILES "$<IF:${baker},${dir}/fast_grass_baker.cpp,${dir}/fast_grass_baker_stub.cpp>")
