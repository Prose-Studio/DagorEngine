# The daScript AOT compiler of daNetGame's games (DagorDas.cmake): daScript with the C++ bindings of the framework's
# modules, which a game's compiler (dagor_add_dng_game in a DAGOR_DAS_AOT_COMPILER tree) links with its own. An object
# library: its modules register themselves, nothing references them.

set(P ${DAGOR_PROG_DIR})
dagor_add_target(NAME daNetGame-das-aot OBJECT LAX
  FILES_CMAKE daNetGame-das-aot_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${P}/daNetGame ${P}/daNetGameLibs ${P}/3rdPartyLibs/rapidjson/include ${P}/engine/dagorInclude
    ${P}/gameLibs/publicInclude ${P}/gameLibs ${P}/1stPartyLibs/daScript/include ${P}/gameLibs/publicInclude/quirrel
    ${P}/1stPartyLibs/quirrel/quirrel/include ${P}/1stPartyLibs/jsoncpp/include ${P}/1stPartyLibs/rapidJsonUtils/include
    ${P}/3rdPartyLibs/recastnavigation/Detour/Include
  COMPILE_DEFINITIONS PUBLIC DAS_AOT_COMPILER
  BUILD_DEPENDENCIES
    PUBLIC
      engine.osApiWrappers engine.kernel engine.perfMon engine.math engine.gameRes engine.memory.rtl engine.consoleProc
      engine.drv.drv3d_null engine.baseUtil engine.startup engine.coreUtil engine.scene engine.imgui.stub
      engine.animChar.stub 3rdPartyLibs.eastl 1stPartyLibs.rapidJsonUtils 1stPartyLibs.daScript
      1stPartyLibs.daScriptModules.rapidjson 1stPartyLibs.daScript.modules.dasImgui
      1stPartyLibs.daScript.modules.dasQuirrel gameLibs.ecs.game.generic gameLibs.ecs.game.zones gameLibs.ecs.net
      engine.daECS.core engine.daECS.gameResStub engine.daECS.io.datablock engine.daECS.utility gameLibs.ecs.scripts.das
      gameLibs.dasModules.common gameLibs.dasModules.quirrel gameLibs.dasModules.phys
      gameLibs.dasModules.projectiveDecals gameLibs.dasModules.ECSGlobalTags gameLibs.dasModules.currentCircuit
      gameLibs.dasModules.gameMath gameLibs.dasModules.generic gameLibs.dasModules.sound
      gameLibs.dasModules.sound.common gameLibs.soundSystem.stub gameLibs.ecs.sound.stub gameLibs.dasModules.shaders
      gameLibs.dasModules.rendInst gameLibs.dasModules.daInput gameLibs.dasModules.actions
      gameLibs.dasModules.daProfiler gameLibs.dasModules.camera gameLibs.dasModules.render gameLibs.dasModules.stdGui
      gameLibs.dasModules.stdGui.aotStub gameLibs.dasModules.imgui gameLibs.dasModules.videoPlayer
      gameLibs.dasModules.gpuReadbackQuery gameLibs.dasModules.landMesh gameLibs.dasModules.systemInfo
      gameLibs.dasModules.compressionUtils gameLibs.dasModules.localization gameLibs.daGame.timers engine.daECS.net
      gameLibs.grid gameLibs.jsonUtils gameLibs.ecs.scripts.sq gameLibs.quirrel.bindQuirrelEx
      gameLibs.quirrel.quirrel_json gameLibs.quirrel.sqCrossCall gameLibs.spacePartition.looseGrid gameLibs.streaming
      gameLibs.dasModules.forceFeedback gameLibs.dasModules.net gameLibs.dasModules.clientNet gameLibs.dasModules.statsd
      gameLibs.daEditorE gameLibs.dasModules.daEditor gameLibs.propsRegistry gameLibs.statsd gameLibs.compressionUtils
      gameLibs.landMesh.stub gameLibs.gamePhys.collision.stub gameLibs.gamePhys.phys.stub gameLibs.gamePhys.props.stub
      gameLibs.render.debug3dSolid.stub gameLibs.dasModules.perFrameStat Dagor::Phys
    PRIVATE Dagor::Quirrel
)
