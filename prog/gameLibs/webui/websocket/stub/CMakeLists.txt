# The web UI's websocket stream without a server (platforms without mongoose)
dagor_add_target(NAME gameLibs.webui.websocket.stub STATIC
  FILES_CMAKE stub_files.cmake
)
