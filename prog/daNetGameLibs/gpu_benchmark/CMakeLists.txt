if(DAGOR_GAME_RENDERER)
  list(APPEND pull_vars gpu_benchmark_ui)
endif()
dagor_add_dng_module(NAME daNetGameLibs.gpu_benchmark
  FILES_CMAKE gpu_benchmark_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR} ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  BUILD_DEPENDENCIES PRIVATE gameLibs.render.gpuBenchmark
  PULL_VARS ${pull_vars}
)
