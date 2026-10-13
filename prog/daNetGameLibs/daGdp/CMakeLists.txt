dagor_add_dng_module(NAME daNetGameLibs.daGdp
  FILES_CMAKE daGdp_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/rendInst
    ${DAGOR_PROG_DIR}/daNetGame ${DAGOR_PROG_DIR}/engine ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui
  # the debug windows' ImGui in Dev and Dbg
  BUILD_DEPENDENCIES PRIVATE gameLibs.render.daFrameGraph gameLibs.rendInst "$<$<CONFIG:Dev,Dbg>:3rdPartyLibs.imgui>"
)
