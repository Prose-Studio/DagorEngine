# daFrameGraph: the render graph (node registry, IR, scheduling of passes, resources and barriers, runtime), with its
# debug visualization in Dev and Dbg, and the features of DAGOR_DAFG_FEATURES: das (daScript bindings), ecs (daECS
# node integration); a game's has both (DagorGame.cmake).
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude . ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui
  ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include)
# the debug tools' libraries in Dev and Dbg (daFrameGraph_files.cmake), the console variables in every configuration
set(deps 3rdPartyLibs.imgui 3rdPartyLibs.imgui-node-editor engine.imgui engine.imgui.util gameLibs.graphLayouter
  gameLibs.render.texDebug)
list(TRANSFORM deps REPLACE "^(.+)$" "$<$<CONFIG:Dev,Dbg>:\\1>")
list(APPEND deps engine.consoleProc)
foreach(feature IN LISTS DAGOR_DAFG_FEATURES)
  if(feature STREQUAL "das")
    list(APPEND includes ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include)
    list(APPEND deps 1stPartyLibs.daScript)
  elseif(NOT feature STREQUAL "ecs")
    message(FATAL_ERROR "DAGOR_DAFG_FEATURES: daFrameGraph has no feature '${feature}'")
  endif()
endforeach()
set(options)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  # warnings that some build systems enable by default: catching them here saves a round trip
  set(options -Wc++11-narrowing -Wswitch -Wbitfield-constant-conversion -Wunused -Wno-unused-local-typedef
    -Wno-unused-but-set-variable)
endif()

dagor_add_target(NAME gameLibs.render.daFrameGraph STATIC
  FILES_CMAKE daFrameGraph_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
