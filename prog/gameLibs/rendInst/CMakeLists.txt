# Render instances: generated and placed instances (rendinst cells, extra instances, impostors, destruction), their
# collision, visibility and rendering. Dedicated servers (DAGOR_DEDICATED) have no impostor textures.
set(defines VECMATH_NO_FMA) # v_madd on NEON is explicit vfmaq that ignores ffp-contract=off
if(DAGOR_BUILDING_TOOLS)
  list(APPEND defines _TARGET_PC_TOOLS_BUILD)
endif()
set(options)
# no fused multiply-adds: the generated positions must match on every platform (contract=off alone does not stop
# the backend from fusing under fast-math)
dagor_deterministic_fp(options KEEP_TRAPPING_MATH)

# the debug mesh rendering outside Rel
dagor_add_target(NAME gameLibs.rendInst STATIC
  FILES_CMAKE rendInst_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/engine/sharedInclude ${CMAKE_CURRENT_SOURCE_DIR}
  COMPILE_DEFINITIONS PRIVATE ${defines}
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE
    gameLibs.render.texcompressors gameLibs.render.primitiveObjects gameLibs.render.debug3dSolid
    gameLibs.render.pointLod engine.lib3d engine.libFx engine.consoleProc 3rdPartyLibs.regExp gameLibs.gpuObjects
    gameLibs.gameMath gameLibs.landMesh.rendinstIntegration gameLibs.resourcePool
    "$<IF:$<CONFIG:Rel>,gameLibs.render.debugMesh.stub,gameLibs.render.debugMesh>"
  PROPERTIES DAGOR_FRAME_LIMIT 262144
)
