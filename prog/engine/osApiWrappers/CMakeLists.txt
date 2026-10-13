# OS API wrappers: files, threads, sync, sockets, dynamic libs, debug output, clipboard, message box.
#
# On Linux the window title and clipboard come from engine/osApiWrappers/linuxGUI in programs with a GUI and from
# stubs otherwise. A program chooses with the DAGOR_LINUX_GUI target property (dagor_add_target(... PROPERTIES
# DAGOR_LINUX_GUI ON); dagor_add_dng_game sets it for the games and editors that render); see dagor_add_link_choice().
set(includes)
set(deps)
set(libs)
set(options)
if(WIN32)
  set(deps engine.osApiWrappers.messageBox)
  set(libs System::shell32 System::version)
elseif(APPLE)
  set(deps engine.osApiWrappers.messageBox)
  set(options -Wno-error)
elseif(ANDROID)
  list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/libunwind/include)
  set(deps engine.osApiWrappers.messageBox.stub 3rdPartyLibs.libunwind)
elseif(LINUX)
  # the GUI or the stubs, by the DAGOR_LINUX_GUI property of the program this ends up in
  dagor_add_target(NAME engine.osApiWrappers.noGUI STATIC
    FILES_CMAKE noGUI_files.cmake
    INCLUDE_DIRECTORIES PRIVATE ${includes}
    COMPILE_DEFINITIONS PRIVATE __B_KERNEL_LIB
  )
  dagor_add_link_choice(engine.osApiWrappers.linuxShell PROPERTY DAGOR_LINUX_GUI
    ON engine.osApiWrappers.linuxGUI OFF engine.osApiWrappers.noGUI)
  set(deps engine.osApiWrappers.linuxShell)
endif()

dagor_add_target(NAME engine.osApiWrappers STATIC
  FILES_CMAKE osApiWrappers_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE __B_KERNEL_LIB
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES
    PUBLIC ${libs}
    PRIVATE ${deps}
)
