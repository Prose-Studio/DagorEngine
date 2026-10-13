set(includes ${CMAKE_CURRENT_SOURCE_DIR})
if(WIN32)
  list(APPEND includes _build_win32)
  list(APPEND c_options -D_CRT_SECURE_NO_WARNINGS -DWINSOCK_DEPRECATED_NO_WARNINGS /wd4267)
elseif(LINUX)
  list(APPEND includes _build_linux)
elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND includes _build_macosx)
else()
  message(FATAL_ERROR "3rdPartyLibs/miniupnpc: no ${CMAKE_SYSTEM_NAME} support")
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
  list(APPEND c_options -Wno-unused-parameter)
endif()
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  list(APPEND c_options -Wno-discarded-qualifiers)
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND c_options -Wno-incompatible-pointer-types-discards-qualifiers)
endif()
list(APPEND c_options -DMINIUPNPC_SET_SOCKET_TIMEOUT -DMINIUPNPC_GET_SRC_ADDR)

dagor_add_target(NAME 3rdPartyLibs.miniupnpc STATIC LAX
  FILES_CMAKE miniupnpc_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_OPTIONS PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
)
