set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR} shaders)
set(deps engine.lib3d)
set(AllSrcFolder_CPP .)

dagor_add_dng_module(gameLibs.voxelizedMedia CPP_DIRS ${AllSrcFolder_CPP})
target_include_directories(gameLibs.voxelizedMedia PRIVATE ${includes})
target_link_libraries(gameLibs.voxelizedMedia PRIVATE ${deps})
