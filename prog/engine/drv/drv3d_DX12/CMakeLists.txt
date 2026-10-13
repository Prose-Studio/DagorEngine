# The Direct3D 12 driver (Windows x64 and arm64) on the Agility SDK, with its GPU crash reporting (DRED, AGS, Aftermath),
# the capture tools' integration and the upscalers (FidelityFX FSR on x64; XeSS has its stub: the fork has no
# 3rdPartyLibs/xess_sdk). The programs that link it ship the Agility, AGS and FidelityFX runtime next to them.
set(deps engine.drv.drv3d_commonCode engine.drv.shadersMetaData.dxil engine.shaders 1stPartyLibs.jsoncpp)

# the Agility SDK's d3d12.h comes before the Windows SDK's
find_package(Agility REQUIRED)
list(APPEND deps Agility::Agility)
find_package(NVAPI)
if(TARGET NVAPI::NVAPI)
  list(APPEND deps NVAPI::NVAPI)
endif()
if(DAGOR_ARCH STREQUAL "x86_64")
  # AMD GPU Services: markers for crash reports, Radeon GPU Profiler captures
  find_package(AGS REQUIRED)
  list(APPEND deps AGS::AGS)
  find_package(Aftermath REQUIRED)
  list(APPEND deps Aftermath::Aftermath)
  # FidelityFX FSR upscaling and frame generation
  find_package(FidelityFX REQUIRED)
  list(APPEND deps FidelityFX::FidelityFX)
endif()

dagor_add_target(NAME engine.drv.drv3d_DX12 STATIC
  FILES_CMAKE drv3d_DX12_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/engine/drv/drv3d_commonCode
    ${DAGOR_PROG_DIR}/engine/drv/drv3d_DX12 ${DAGOR_PROG_DIR}/engine/shaders ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui
    ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  COMPILE_DEFINITIONS PRIVATE INSIDE_DRIVER D3DX12_NO_STATE_OBJECT_HELPERS
  BUILD_DEPENDENCIES PRIVATE ${deps}
  FORCE_INCLUDES d3d_config.h
  PROPERTIES DAGOR_FRAME_LIMIT 262144
)
