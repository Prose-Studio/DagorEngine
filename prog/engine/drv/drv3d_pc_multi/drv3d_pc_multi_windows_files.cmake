# the HLSL compiler of the DirectX drivers
if("DX11" IN_LIST DAGOR_D3D_DRIVERS OR "DX12" IN_LIST DAGOR_D3D_DRIVERS)
  set(FILES hlsl_dx.cpp)
else()
  set(FILES hlsl_stub.cpp)
endif()
