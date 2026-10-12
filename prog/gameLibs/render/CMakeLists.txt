# The shared rendering code of games and tools: post effects, shadows, sky, clouds, decals, texture utilities and more.
# Outside Rel it also has the ImGui GPU profiler and the debug mesh rendering.
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
