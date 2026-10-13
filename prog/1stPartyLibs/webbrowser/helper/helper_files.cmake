set(FILES main.cpp endpoint.cpp cef/app.cpp cef/client.cpp cef/browserList.cpp cef/cookies.cpp cef/javaScriptHandler.cpp
  helper.rc)
if(DAGOR_ARCH STREQUAL "x86_64")
  list(APPEND FILES helper64.exe.manifest)
endif()
