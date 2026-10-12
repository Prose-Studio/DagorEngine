add_subdirectory(stub)

set(sources imguiInput.cpp imguiInputHandler.cpp)
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(deps 3rdPartyLibs.eastl 3rdPartyLibs.imgui engine.imgui gameLibs.daInput)

dagor_add_library(gameLibs.imguiInput LAX ${sources})
target_include_directories(gameLibs.imguiInput PRIVATE ${includes})
target_link_libraries(gameLibs.imguiInput PRIVATE ${deps})
