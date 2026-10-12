# daFrameGraph: the render graph (node registry, IR, scheduling of passes, resources and barriers, runtime), with its
# debug visualization in Dev and Dbg, and the features of DAGOR_DAFG_FEATURES: das (daScript bindings), ecs (daECS
# node integration); a game's has both (DagorGame.cmake).
if(DAGOR_ENGINE_TESTS)
  add_subdirectory(tests)
endif()

set(sources
  api/cpp/detail/virtualResourceHandleBase.cpp
  api/cpp/detail/virtualResourceRequestBase.cpp
  api/cpp/detail/dispatchRequestBase.cpp
  api/cpp/detail/drawRequestBase.cpp
  api/cpp/daFG.cpp
  api/cpp/baseRegistry.cpp
  api/cpp/stateRequest.cpp
  api/cpp/virtualPassRequest.cpp
  api/cpp/autoResolutionRequest.cpp
  api/cpp/nameSpace.cpp
  api/cpp/nameSpaceRequest.cpp
  common/resourceUsage.cpp
  frontend/dependencyDataCalculator.cpp
  frontend/nodeTracker.cpp
  frontend/irGraphBuilder.cpp
  frontend/nameResolver.cpp
  frontend/multiplexingInternal.cpp
  frontend/dumpInternalRegistry.cpp
  frontend/registryValidator.cpp
  frontend/dynamicResolution.cpp
  backend/intermediateRepresentation.cpp
  backend/nodeStateDeltas.cpp
  backend/passColoring.cpp
  backend/nodeScheduler.cpp
  backend/resourceScheduling/resourceLifetimes.cpp
  backend/resourceScheduling/heapLayout.cpp
  backend/resourceScheduling/layoutOptimizer.cpp
  backend/resourceScheduling/layoutUpdate.cpp
  backend/resourceScheduling/heapPolicy.cpp
  backend/resourceScheduling/barrierScheduler.cpp
  backend/resourceScheduling/resourceScheduler.cpp
  backend/resourceScheduling/resourceAllocator.cpp
  backend/resourceScheduling/nativeResourceAllocator.cpp
  backend/resourceScheduling/poolResourceAllocator.cpp
  backend/blobBindingHelpers.cpp
  backend/badResolutionTracker.cpp
  runtime/graphHierarchicalMarksParser.cpp
  runtime/nodeExecutor.cpp
  runtime/typeDb.cpp
  runtime/runtime.cpp
  runtime/bindlessSlotManager.cpp
)
set(dir "${CMAKE_CURRENT_SOURCE_DIR}")

# the debug tools in Dev and Dbg; the per-node global state validation only with checked containers there too
set(debug_sources
  debug/resourceValidation.cpp debug/textureVisualization.cpp debug/backendDebug.cpp debug/gpuRangeCapture.cpp
  debug/jsonDump.cpp debug/jsonDumpCommon.cpp debug/jsonDumpRegistry.cpp debug/jsonDumpIntermediate.cpp
  debug/jsonDumpStateDeltas.cpp debug/visualizationManager.cpp debug/visualization/structuresCommon.cpp
  debug/visualization/userGraphVisualizer.cpp debug/visualization/irGraphVisualizer.cpp
  debug/visualization/resourceVisualizer.cpp debug/visualization/textureVisualizer.cpp
  debug/visualization/gpuCaptureWindow.cpp)
set(debug "$<CONFIG:Dev,Dbg>")
# one generator expression per file: a list inside one would be split before it is evaluated
list(TRANSFORM debug_sources REPLACE "^(.+)$" "$<${debug}:${dir}/\\1>")
list(APPEND sources ${debug_sources}
  "$<$<NOT:${debug}>:${dir}/debug/stub/backendDebugStub.cpp>"
  "$<$<NOT:${debug}>:${dir}/debug/stub/gpuRangeCaptureStub.cpp>")
set(checked "$<CONFIG:${DAGOR_CHECKED_CONTAINERS_CONFIGS}>")
if(NOT DAGOR_CHECKED_CONTAINERS_CONFIGS)
  set(checked 0)
else()
  string(REPLACE ";" "," checked "${checked}")
endif()
list(APPEND sources
  "$<IF:$<AND:${debug},${checked}>,${dir}/debug/globalStatesValidation.cpp,${dir}/debug/stub/globalStatesValidationStub.cpp>")
set(deps 3rdPartyLibs.imgui 3rdPartyLibs.imgui-node-editor engine.imgui engine.imgui.util gameLibs.graphLayouter
  gameLibs.render.texDebug)
list(TRANSFORM deps REPLACE "^(.+)$" "$<${debug}:\\1>")
list(APPEND deps engine.consoleProc) # its console variables, in every configuration

set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude . ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui
  ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include)
set(defines)
set(es)
foreach(feature IN LISTS DAGOR_DAFG_FEATURES)
  if(feature STREQUAL "das")
    list(APPEND sources api/das/enumerations.cpp api/das/frameGraphModule.cpp api/das/nodeDataAnnotation.cpp
      api/das/structureAnnotations.cpp api/das/blobBindings.cpp api/das/blobInterop.cpp)
    list(APPEND includes ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include)
    list(APPEND deps 1stPartyLibs.daScript)
  elseif(feature STREQUAL "ecs")
    set(es api/ecs/frameGraphNodeES.cpp.inl)
  else()
    message(FATAL_ERROR "DAGOR_DAFG_FEATURES: daFrameGraph has no feature '${feature}'")
  endif()
endforeach()
set(options)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  # warnings that some build systems enable by default: catching them here saves a round trip
  set(options -Wc++11-narrowing -Wswitch -Wbitfield-constant-conversion -Wunused -Wno-unused-local-typedef
    -Wno-unused-but-set-variable)
endif()

set(name gameLibs.render.daFrameGraph)
dagor_add_library(${name} ${sources})
target_include_directories(${name} PRIVATE ${includes})
target_compile_definitions(${name} PRIVATE ${defines})
target_compile_options(${name} PRIVATE ${options})
target_link_libraries(${name} PRIVATE ${deps})
dagor_target_es_sources(${name} ${es})
