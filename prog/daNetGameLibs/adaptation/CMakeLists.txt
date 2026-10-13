set(deps)
if(DAGOR_GAME_RENDERER)
  # the debug window's ImGui in Dev and Dbg
  set(deps gameLibs.render.adaptation "$<$<CONFIG:Dev,Dbg>:3rdPartyLibs.imgui>")
endif()
dagor_add_dng_module(NAME daNetGameLibs.adaptation
  FILES_CMAKE adaptation_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
