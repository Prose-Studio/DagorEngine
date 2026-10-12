# os_message_box() stub: no message box, always GUI_MB_FAIL (programs without a GUI)
set(defines __B_KERNEL_LIB __B_NO_MEM_BASE_INCLUDE)
set(sources messageBox.cpp)
list(APPEND includes ${DAGOR_PROG_DIR}/engine/sharedInclude)

dagor_add_library(engine.osApiWrappers.messageBox.stub ${sources})
target_include_directories(engine.osApiWrappers.messageBox.stub PRIVATE ${includes})
target_compile_definitions(engine.osApiWrappers.messageBox.stub PRIVATE ${defines})
