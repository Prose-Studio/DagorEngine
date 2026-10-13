# The engine's 3d layer above the driver: texture and buffer managers, DDSx loading, debug drawing, occlusion
# (masked occlusion culling), texture streaming
set(defines)
set(deps 3rdPartyLibs.eastl "$<$<CONFIG:Dev,Dbg>:engine.consoleProc>")
if(WIN32)
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

dagor_add_target(NAME engine.lib3d STATIC
  FILES_CMAKE lib3d_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/binPack2D/include ${DAGOR_PROG_DIR}/engine/drv/drv3d_commonCode
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PRIVATE ${deps}
  PROPERTIES DAGOR_FRAME_LIMIT 262144
)
