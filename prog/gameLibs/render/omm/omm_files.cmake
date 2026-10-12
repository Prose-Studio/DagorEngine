if((WIN32 OR LINUX) AND DAGOR_ARCH STREQUAL "x86_64")
  set(FILES
    omm.cpp
    omm_cpu.cpp
    omm_debug.cpp
    ../../../3rdPartyLibs/omm_sdk/src/bake.cpp
    ../../../3rdPartyLibs/omm_sdk/src/bake_cpu_impl.cpp
    ../../../3rdPartyLibs/omm_sdk/src/bake_gpu_impl.cpp
    omm_sdk_debug_stub.cpp
    ../../../3rdPartyLibs/omm_sdk/src/serialize_impl.cpp
    ../../../3rdPartyLibs/omm_sdk/src/shader_bindings.cpp
    ../../../3rdPartyLibs/omm_sdk/src/texture_impl.cpp
  )
else()
  set(FILES omm_stub.cpp)
endif()
