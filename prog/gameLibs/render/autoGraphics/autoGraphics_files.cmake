if(CMAKE_SYSTEM_NAME MATCHES "^(Linux|Windows)$")
  set(FILES
    cpuBenchmark.cpp
    autoQualityPreset.cpp
    gpuDatabase/sampler.cpp
    presetDatabase/sampler.cpp
    autoResolution.cpp
    autoAntialiasing.cpp
  )
else()
  set(FILES cpuBenchmarkStub.cpp autoGraphicsStub.cpp)
endif()
