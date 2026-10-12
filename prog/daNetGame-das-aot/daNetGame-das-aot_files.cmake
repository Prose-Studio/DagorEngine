# the framework's daScript modules (P: the engine's prog dir)
set(FILES
  ${P}/daNetGame-das-aot/main.cpp
  ${P}/daNetGame-das-aot/da.cpp

  ${P}/1stPartyLibs/daScript/dagorAdapter/da_dummy.cpp
  ${P}/daNetGame/dasModules/actor.cpp
  ${P}/daNetGame/dasModules/app.cpp
  ${P}/daNetGame/dasModules/testMode.cpp
  ${P}/gameLibs/dasModules/auth/auth.cpp
  ${P}/gameLibs/dasModules/appTime/appTime.cpp
  ${P}/daNetGame/dasModules/camera.cpp
  ${P}/daNetGame/dasModules/cameraShaker.cpp
  ${P}/daNetGame/dasModules/capsuleApproximation.cpp
  ${P}/daNetGame/dasModules/collisionTraces.cpp
  ${P}/daNetGame/dasModules/dagorDebug3dSolid.cpp
  ${P}/daNetGame/dasModules/dgNet.cpp
  ${P}/daNetGame/dasModules/dngHostedServer.cpp
  ${P}/daNetGame/dasModules/gameObject.cpp
  ${P}/daNetGame/dasModules/gridCollision.cpp
  ${P}/daNetGame/dasModules/level.cpp
  ${P}/daNetGame/dasModules/netPhys.cpp
  ${P}/daNetGame/dasModules/propsRegistry.cpp
  ${P}/daNetGame/dasModules/netPropsRegistry.cpp
  ${P}/daNetGame/dasModules/netstat.cpp
  ${P}/daNetGame/dasModules/phys.cpp
  ${P}/daNetGame/dasModules/player.cpp
  ${P}/daNetGame/dasModules/replay.cpp
  ${P}/daNetGame/dasModules/scene.cpp
  ${P}/daNetGame/dasModules/smokeOccluder.cpp
  ${P}/daNetGame/dasModules/sound/aotSoundProps.cpp
  ${P}/daNetGame/dasModules/sound_net/aotSoundNetProps.cpp
  ${P}/daNetGame/dasModules/streaming.cpp
  ${P}/daNetGame/dasModules/ui.cpp
  ${P}/daNetGame/dasModules/dacoll.cpp
  ${P}/daNetGame/dasModules/matchingTypes.cpp
  ${P}/daNetGame/input/dasModules/touchInput.cpp
  ${P}/daNetGame/render/dasModules/clipmapDecals.cpp
  ${P}/daNetGame/render/dasModules/daSkies.cpp
  ${P}/daNetGame/render/dasModules/fx.cpp
  ${P}/daNetGame/render/dasModules/priorityManagedShadervar.cpp
  ${P}/daNetGame/render/dasModules/dagorMaterials.cpp
  ${P}/daNetGame/render/dasModules/worldRenderer.cpp
  ${P}/daNetGame/render/dasModules/heightmapQueryManager.cpp
  ${P}/daNetGame/render/dasModules/portalRenderer.cpp
  ${P}/daNetGame/render/dasModules/bvh.cpp

  ${P}/daNetGame/main/dedicated/dasModules/dngMatching.cpp

  ${P}/daNetGame-das-aot/stub.cpp
  ${P}/gameLibs/daRg/dasBinding.cpp

  ${P}/1stPartyLibs/daScript/modules/dasStdDlg/src/dasStdDlg.cpp
  ${P}/1stPartyLibs/daScript/modules/dasStdDlg/src/dasStdDlgNotImplemented.cpp
  ${P}/1stPartyLibs/daScript/modules/dasStdDlg/src/dasStdDlgTray.cpp
  ${P}/1stPartyLibs/daScript/modules/dasStdDlg/src/dasStdDlgTrayNotImplemented.cpp

  # the daScript bindings of libraries (their _aot.jam)
  ${P}/gameLibs/render/outline/dasModules/outline.cpp
  ${P}/gameLibs/rendInst/aot/stub.cpp
  ${P}/gameLibs/daEditorE/aot/stub.cpp
)
# those that include their library's private headers (from the library's dir)
foreach(group
    "gameLibs/render/daFrameGraph:api/das/frameGraphModule.cpp;api/das/enumerations.cpp;api/das/nodeDataAnnotation.cpp;api/das/structureAnnotations.cpp;api/das/blobBindings.cpp;api/das/stub_aot.cpp"
    "gameLibs/render/resourceSlot:das/resourceSlotCoreModule.cpp;das/stub_aot.cpp"
    "gameLibs/ecs/deferToAct:deferToActModule.cpp;stub_aot.cpp")
  string(REGEX MATCH "^[^:]+" lib "${group}")
  string(REGEX REPLACE "^[^:]+:" "" files "${group}")
  list(TRANSFORM files PREPEND "${P}/${lib}/")
  set_property(SOURCE ${files} APPEND PROPERTY INCLUDE_DIRECTORIES "${P}/${lib}")
  list(APPEND FILES ${files})
endforeach()
if(CMAKE_SYSTEM_NAME MATCHES "^(Darwin|Linux|Windows)$")
  list(APPEND FILES ${P}/daNetGame/dasModules/websocket/webSocket.cpp
    ${P}/daNetGame/dasModules/websocket/webSocketServer.cpp)
endif()
set(STRINGIFY_FILES ${P}/daNetGame/dasModules/dgNet.das ${P}/daNetGame/dasModules/dagorDebug3dSolid.das
  ${P}/daNetGame/render/dasModules/daSkies.das ${P}/daNetGame/render/dasModules/fx.das)
if(CMAKE_SYSTEM_NAME MATCHES "^(Darwin|Linux|Windows)$")
  list(APPEND STRINGIFY_FILES ${P}/daNetGame/dasModules/websocket/webSocket.das)
endif()
