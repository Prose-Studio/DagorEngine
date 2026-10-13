# Eye adaptation (exposure) of the HDR render, with its debug window in Dev and Dbg
dagor_add_target(NAME gameLibs.render.adaptation STATIC
  FILES_CMAKE adaptation_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR} ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui
)
