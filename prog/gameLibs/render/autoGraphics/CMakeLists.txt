set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
if(CMAKE_SYSTEM_NAME MATCHES "^(Linux|Windows)$")
  set(sources
    cpuBenchmark.cpp
    autoQualityPreset.cpp
    gpuDatabase/sampler.cpp
    presetDatabase/sampler.cpp
    autoResolution.cpp
    autoAntialiasing.cpp
  )
else()
  set(sources cpuBenchmarkStub.cpp autoGraphicsStub.cpp)
endif()

dagor_add_library(gameLibs.render.autoGraphics ${sources})
target_include_directories(gameLibs.render.autoGraphics PRIVATE ${includes})
set_target_properties(gameLibs.render.autoGraphics PROPERTIES DAGOR_FRAME_LIMIT 262144)
