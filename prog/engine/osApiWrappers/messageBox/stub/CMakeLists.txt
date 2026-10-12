# os_message_box() stub: no message box, always GUI_MB_FAIL (programs without a GUI)
dagor_add_target(NAME engine.osApiWrappers.messageBox.stub STATIC
  FILES_CMAKE stub_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
  COMPILE_DEFINITIONS PRIVATE __B_KERNEL_LIB __B_NO_MEM_BASE_INCLUDE
)
