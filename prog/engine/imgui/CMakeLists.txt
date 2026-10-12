# The engine's ImGui integration: platform input, the renderer, the test runtime, netImgui outside Rel. Programs that
# set DAGOR_IMGUI_TEST_ENGINE get the build with the ImGui test engine hooks (see 3rdPartyLibs/imgui).
add_subdirectory(stub)
add_subdirectory(util)

include(netImgui.cmake)
foreach(build standard testEngine)
  set(defines ${NET_IMGUI_DEFINES})
  if(build STREQUAL "testEngine")
    list(APPEND defines IMGUI_ENABLE_TEST_ENGINE)
  endif()
  dagor_add_target(NAME engine.imgui.${build} STATIC LAX
    FILES_CMAKE imgui_files.cmake
    INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude ${NET_IMGUI_INCLUDES}
    COMPILE_DEFINITIONS PRIVATE ${defines}
    BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.imgui ${NET_IMGUI_DEPS}
  )
endforeach()
dagor_add_link_choice(engine.imgui PROPERTY DAGOR_IMGUI_TEST_ENGINE ON engine.imgui.testEngine OFF engine.imgui.standard)
