set(FILES sqmodules.cpp path.cpp helpers.cpp)
if(CMAKE_SYSTEM_NAME MATCHES "^(Darwin|Linux|Windows)$")
  list(APPEND FILES deffileaccess.cpp)
endif()
