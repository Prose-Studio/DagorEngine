set(FILES simplePBlock.cpp base64.cpp localization.cpp)
if(NOT ANDROID OR TRUE)
  list(APPEND FILES flyMode.cpp)
endif()
