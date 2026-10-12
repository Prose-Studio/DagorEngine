# The shared rendering code of games and tools: post effects, shadows, sky, clouds, decals, texture utilities and more.
# Outside Rel it also has the ImGui GPU profiler and the debug mesh rendering.
add_subdirectory(ambientOcclusion)
add_subdirectory(animCharTexReplace)
add_subdirectory(animatedSplashScreen)
add_subdirectory(antialiasing)
add_subdirectory(autoGraphics)
add_subdirectory(cables)
add_subdirectory(cameraInCamera)
add_subdirectory(camouflage)
add_subdirectory(daFrameGraph)
add_subdirectory(debug3dSolid)
add_subdirectory(debugMesh)
add_subdirectory(debugMultiTextLabels)
add_subdirectory(denoiser)
add_subdirectory(deviceResetTelemetry)
add_subdirectory(dof)
add_subdirectory(dynmodelRenderer)
add_subdirectory(enviCover)
add_subdirectory(fastGrassBaker)
add_subdirectory(foam)
add_subdirectory(fx)
add_subdirectory(genericLUT)
add_subdirectory(hdrRender)
add_subdirectory(heatHaze)
add_subdirectory(imGuiProfiler)
add_subdirectory(indoorProbes)
add_subdirectory(levelProfiler)
add_subdirectory(lights)
add_subdirectory(lruCollision)
add_subdirectory(metronome)
add_subdirectory(nodeBasedShader)
add_subdirectory(objectMotionBlur)
add_subdirectory(occlusion)
add_subdirectory(omm)
add_subdirectory(outline)
add_subdirectory(pointLod)
add_subdirectory(primitiveObjects)
add_subdirectory(psoCacheLoader)
add_subdirectory(ptgi)
add_subdirectory(quirrel)
add_subdirectory(rainX7)
add_subdirectory(resourceSlot)
add_subdirectory(rtao)
add_subdirectory(rtr)
add_subdirectory(rtsm)
add_subdirectory(shaderCacheWarmup)
add_subdirectory(texDebug)
add_subdirectory(texcompressors)
add_subdirectory(tracer)
add_subdirectory(upscale)
add_subdirectory(volumetricLights)
add_subdirectory(voxelizationTarget)
add_subdirectory(wakePs)
add_subdirectory(waterRipples)
add_subdirectory(wind)
list(APPEND deps engine.lib3d gameLibs.render.lights gameLibs.render.texcompressors gameLibs.render.primitiveObjects
  gameLibs.render.fx gameLibs.frustumCulling gameLibs.render.dynmodelRenderer gameLibs.resourcePool)
list(APPEND deps "$<IF:$<CONFIG:Rel>,gameLibs.render.imGuiProfiler.stub,gameLibs.render.imGuiProfiler>"
  "$<IF:$<CONFIG:Rel>,gameLibs.render.debugMesh.stub,gameLibs.render.debugMesh>")
if(WIN32)
  list(APPEND libs System::oleaut32)
endif()

dagor_add_target(NAME gameLibs.render STATIC
  FILES_CMAKE render_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/binPack2D/include
    ${CMAKE_CURRENT_SOURCE_DIR} shaders ${DAGOR_PROG_DIR}/commonFx/commonFxGame
  BUILD_DEPENDENCIES
    PUBLIC ${libs}
    PRIVATE ${deps}
  PROPERTIES DAGOR_FRAME_LIMIT 262144
)
