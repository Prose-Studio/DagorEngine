# The ray tracing denoiser (NRD), part of the BVH stack (DAGOR_GAME_BVH), or its stub. MathLib trips MSVC's C4587 in
# ml::float4x4, which warnings-as-errors make fatal: with MSVC, the stub.
set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/3rdPartyLibs/math/sse2neon
  ${DAGOR_PROG_DIR}/3rdPartyLibs/math/MathLib
  ${DAGOR_PROG_DIR}/3rdPartyLibs/NRD
)
if(NOT DAGOR_GAME_BVH OR CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  dagor_add_library(gameLibs.render.denoiser denoiser_stub.cpp)
  target_include_directories(gameLibs.render.denoiser PRIVATE ${includes})
  return()
endif()
set(options)
if(LINUX AND DAGOR_SSE LESS 4)
  list(APPEND options -msse4) # one binary for the Linux clients: this lib is always SSE4
endif()
dagor_add_library(gameLibs.render.denoiser denoiser.cpp)
target_include_directories(gameLibs.render.denoiser PRIVATE ${includes})
target_compile_definitions(gameLibs.render.denoiser PRIVATE SSE2NEON_SUPPRESS_WARNINGS # sse2neon's advisory #warning is fatal as an error
)
target_compile_options(gameLibs.render.denoiser PRIVATE ${options})
