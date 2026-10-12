# ENet reliable UDP networking
if(WIN32)
  list(APPEND libs System::winmm System::ws2_32)
elseif(CMAKE_SYSTEM_NAME MATCHES "^(Android|Darwin|Linux|iOS|tvOS)$")
  list(APPEND defines HAS_SOCKLEN_T HAS_POLL HAS_INET_NTOP HAS_INET_PTON HAS_MSGHDR_FLAGS SOMAXCONN=128)
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES "^(Clang|AppleClang|GNU)$")
  list(APPEND options -Wno-unused-parameter)
endif()

dagor_add_target(NAME 3rdPartyLibs.enet STATIC LAX
  FILES_CMAKE enet_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/enet/include
  COMPILE_DEFINITIONS PRIVATE ${defines}
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PUBLIC ${libs}
)
