set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
# the baker on Windows outside Rel and IRel, the stub elsewhere
set(baker 0)
if(WIN32)
  set(baker "$<NOT:$<CONFIG:Rel,IRel>>")
  set(deps "$<${baker}:3rdPartyLibs.image.tiff-4.4.0>" "$<${baker}:3rdPartyLibs.convert.ispc_texcomp>")
  list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/convert/ispc_texcomp ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/gameLibs/rendInst)
endif()
set(dir ${CMAKE_CURRENT_SOURCE_DIR})
set(sources "$<IF:${baker},${dir}/fast_grass_baker.cpp,${dir}/fast_grass_baker_stub.cpp>")

dagor_add_library(gameLibs.render.fastGrassBaker ${sources})
target_include_directories(gameLibs.render.fastGrassBaker PRIVATE ${includes})
target_link_libraries(gameLibs.render.fastGrassBaker PRIVATE ${deps})
