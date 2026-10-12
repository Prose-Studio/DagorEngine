set(FILES
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
# the debug tools in Dev and Dbg; the per-node global state validation only with checked containers there too
set(debug_files
  debug/resourceValidation.cpp debug/textureVisualization.cpp debug/backendDebug.cpp debug/gpuRangeCapture.cpp
  debug/jsonDump.cpp debug/jsonDumpCommon.cpp debug/jsonDumpRegistry.cpp debug/jsonDumpIntermediate.cpp
  debug/jsonDumpStateDeltas.cpp debug/visualizationManager.cpp debug/visualization/structuresCommon.cpp
  debug/visualization/userGraphVisualizer.cpp debug/visualization/irGraphVisualizer.cpp
  debug/visualization/resourceVisualizer.cpp debug/visualization/textureVisualizer.cpp
  debug/visualization/gpuCaptureWindow.cpp)
set(dir "${CMAKE_CURRENT_LIST_DIR}")
set(debug "$<CONFIG:Dev,Dbg>")
# one generator expression per file: a list inside one would be split before it is evaluated
list(TRANSFORM debug_files REPLACE "^(.+)$" "$<${debug}:${dir}/\\1>")
list(APPEND FILES ${debug_files}
  "$<$<NOT:${debug}>:${dir}/debug/stub/backendDebugStub.cpp>"
  "$<$<NOT:${debug}>:${dir}/debug/stub/gpuRangeCaptureStub.cpp>")
set(checked 0)
if(DAGOR_CHECKED_CONTAINERS_CONFIGS)
  string(REPLACE ";" "," checked "$<CONFIG:${DAGOR_CHECKED_CONTAINERS_CONFIGS}>")
endif()
list(APPEND FILES
  "$<IF:$<AND:${debug},${checked}>,${dir}/debug/globalStatesValidation.cpp,${dir}/debug/stub/globalStatesValidationStub.cpp>")

# the features
if("das" IN_LIST DAGOR_DAFG_FEATURES)
  list(APPEND FILES api/das/enumerations.cpp api/das/frameGraphModule.cpp api/das/nodeDataAnnotation.cpp
    api/das/structureAnnotations.cpp api/das/blobBindings.cpp api/das/blobInterop.cpp)
endif()
if("ecs" IN_LIST DAGOR_DAFG_FEATURES)
  set(ES_FILES api/ecs/frameGraphNodeES.cpp.inl)
endif()
