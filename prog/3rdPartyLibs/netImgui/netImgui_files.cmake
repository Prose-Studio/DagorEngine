set(FILES
  source/NetImgui_Api.cpp
  source/NetImgui_Client.cpp
  source/NetImgui_CmdPackets_DrawFrame.cpp
  quicklz/quicklz.cpp
)
if(CMAKE_SYSTEM_NAME MATCHES "^(Android|Darwin|Linux)$")
  list(APPEND FILES source/NetImgui_NetworkPosix.cpp)
endif()
