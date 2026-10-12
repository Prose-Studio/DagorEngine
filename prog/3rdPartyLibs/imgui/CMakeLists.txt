# Dear ImGui with ImPlot and the FreeType font rasterizer. Programs that set the DAGOR_IMGUI_TEST_ENGINE target
# property get the build with the hooks of the ImGui test engine (3rdPartyLibs.imgui.testEngine), see
# dagor_add_link_choice().
set(options)
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND options -Wno-deprecated-declarations)
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  list(APPEND options /wd4756) # C4756: overflow in constant arithmetic
endif()
foreach(build standard testEngine)
  set(defines)
  if(build STREQUAL "testEngine")
    set(defines IMGUI_ENABLE_TEST_ENGINE)
  endif()
  dagor_add_library(3rdPartyLibs.imgui.${build} LAX imgui.cpp imgui_demo.cpp imgui_draw.cpp imgui_widgets.cpp
    imgui_tables.cpp implot.cpp implot_demo.cpp implot_items.cpp misc/freetype/imgui_freetype.cpp)
  target_include_directories(3rdPartyLibs.imgui.${build} PRIVATE .
    ${DAGOR_PROG_DIR}/3rdPartyLibs/freetype/freetype-2.8/include)
  target_compile_definitions(3rdPartyLibs.imgui.${build} PRIVATE ${defines})
  target_compile_options(3rdPartyLibs.imgui.${build} PRIVATE ${options})
  target_link_libraries(3rdPartyLibs.imgui.${build} PRIVATE 3rdPartyLibs.freetype.freetype-2.8)
endforeach()
dagor_add_link_choice(3rdPartyLibs.imgui PROPERTY DAGOR_IMGUI_TEST_ENGINE
  ON 3rdPartyLibs.imgui.testEngine OFF 3rdPartyLibs.imgui.standard)
