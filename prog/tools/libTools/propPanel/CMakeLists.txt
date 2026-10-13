# The property panels of the tools (on ImGui). Programs that set DAGOR_IMGUI_TEST_ENGINE get the build with the hooks
# of the ImGui test engine, see dagor_add_link_choice().
set(libs)
set(includes)
if(LINUX)
  list(APPEND includes
    /usr/include/dbus-1.0
    /usr/lib/x86_64-linux-gnu/dbus-1.0/include
    /usr/lib64/dbus-1.0/include
  )
  list(APPEND libs System::dbus-1)
endif()

foreach(build standard testEngine)
  set(defines)
  if(build STREQUAL "testEngine")
    set(defines IMGUI_ENABLE_TEST_ENGINE)
  endif()
  dagor_add_target(NAME tools.libTools.propPanel.${build} STATIC LAX
    FILES_CMAKE propPanel_files.cmake
    INCLUDE_DIRECTORIES PRIVATE ${includes}
    COMPILE_DEFINITIONS PRIVATE ${defines}
    BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.imgui 3rdPartyLibs.math.srcc_msu engine.imgui.util ${libs}
  )
endforeach()
dagor_add_link_choice(tools.libTools.propPanel PROPERTY DAGOR_IMGUI_TEST_ENGINE
  ON tools.libTools.propPanel.testEngine OFF tools.libTools.propPanel.standard)
