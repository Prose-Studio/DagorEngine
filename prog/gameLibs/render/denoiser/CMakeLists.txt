# The ray tracing denoiser (NRD), part of the BVH stack (DAGOR_GAME_BVH), or its stub. MathLib trips MSVC's C4587 in
# ml::float4x4, which warnings-as-errors make fatal: with MSVC, the stub.
set(options)
if(LINUX AND DAGOR_SSE LESS 4 AND DAGOR_GAME_BVH)
  list(APPEND options -msse4) # one binary for the Linux clients: this lib is always SSE4
endif()
dagor_add_target(NAME gameLibs.render.denoiser STATIC
  FILES_CMAKE denoiser_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/math/sse2neon
    ${DAGOR_PROG_DIR}/3rdPartyLibs/math/MathLib ${DAGOR_PROG_DIR}/3rdPartyLibs/NRD
  # sse2neon's advisory #warning is fatal as an error
  COMPILE_DEFINITIONS PRIVATE SSE2NEON_SUPPRESS_WARNINGS
  COMPILE_OPTIONS PRIVATE ${options}
)
