set(deps gameLibs.rendInst)
if(IS_DIRECTORY "${DAGOR_PROG_DIR}/gameLibs/gamePhys")
  list(APPEND deps
    gameLibs.gameMath
    gameLibs.gamePhys.phys
    gameLibs.gamePhys.props
    gameLibs.gamePhys.collision.collision-common
    gameLibs.gamePhys.collision.rendinst
    gameLibs.gamePhys.common
    gameLibs.gamePhys.phys.destrRender
    gameLibs.daFracture.core
    gameLibs.daFracture.renderStub
  )
  list(APPEND defines HAS_GAME_PHYS)
endif()

dagor_add_target(NAME tools.sceneTools.daEditorX.services.riMgr STATIC LAX
  FILES_CMAKE riMgr_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/rendInst
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
