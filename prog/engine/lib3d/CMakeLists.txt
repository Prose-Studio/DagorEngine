# The engine's 3d layer above the driver: texture and buffer managers, DDSx loading, debug drawing, occlusion
# (masked occlusion culling), texture streaming
add_subdirectory(moc_avx)

set(sources
  texMgr.cpp
  bufMgr.cpp
  texMgrData.cpp
  texMgrCreat.cpp
  texMgrMem.cpp
  texMgrCon.cpp
  tqlInit.cpp
  loadDDSx/texLoad.cpp
  loadDDSx/texResize.cpp
  texMgrMt.cpp
  texMgrFileFactory.cpp
  texMgrSymFactory.cpp
  texMgrStubFactory.cpp
  textureFormat.cpp
  convertPixelFormat.cpp
  regTexCreateRaw.cpp
  regTexCreateTiff.cpp
  drv3dReset.cpp
  setGamma.cpp
  preRotation.cpp
  debug3dBuffered.cpp
  debug3dCached.cpp
  debug3dStates.cpp
  debug3dTex.cpp
  texPackMgr2.cpp
  createTex.cpp
  picMgr.cpp
  splashScreen.cpp
  texIdHolder.cpp
  bufIdHolder.cpp
  resizableTex.cpp
  ringCPUQueryLock.cpp
  MaskedOcclusionCulling.cpp
  occlusionSystem.cpp
  quadIndexBuffer.cpp
  serialIntBuffer.cpp
  texStreamingContext.cpp
  buildOnDemandTexFactory.cpp
)
if(DAGOR_ARCH MATCHES "^(x86_64|e2k)$" AND NOT DAGOR_ARCH STREQUAL "universal")
  list(APPEND sources MaskedOcclusionCulling_sse.cpp)
else()
  list(APPEND sources MaskedOcclusionCulling_neon.cpp)
endif()
set(includes
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/3rdPartyLibs/binPack2D/include
  ${DAGOR_PROG_DIR}/engine/drv/drv3d_commonCode
)
set(defines)
set(deps 3rdPartyLibs.eastl "$<$<CONFIG:Dev,Dbg>:engine.consoleProc>")
if(WIN32)
  list(APPEND sources gpu_pipeline_serialization.cpp)
  find_package(Agility REQUIRED)
  list(APPEND deps Agility::Agility)
  list(APPEND defines D3DX12_NO_STATE_OBJECT_HELPERS) # no wrl
  list(APPEND deps 3rdPartyLibs.convert.detex)
endif()
if(DAGOR_BUILDING_TOOLS)
  list(APPEND defines _TARGET_PC_TOOLS_BUILD)
endif()
if(DAGOR_FORCE_LINK_DEBUG_LINES)
  list(APPEND defines "$<$<CONFIG:Rel,IRel>:FORCE_LINK_DEBUG_LINES>")
endif()
if(CMAKE_SYSTEM_NAME MATCHES "^(Linux|Windows)$" AND DAGOR_ARCH STREQUAL "x86_64" AND DAGOR_SSE EQUAL 4)
  list(APPEND deps engine.lib3d.moc_avx)
endif()

dagor_add_library(engine.lib3d ${sources})
target_include_directories(engine.lib3d PRIVATE ${includes})
target_compile_definitions(engine.lib3d PRIVATE ${defines})
target_link_libraries(engine.lib3d PRIVATE ${deps})
set_target_properties(engine.lib3d PROPERTIES DAGOR_FRAME_LIMIT 262144)
