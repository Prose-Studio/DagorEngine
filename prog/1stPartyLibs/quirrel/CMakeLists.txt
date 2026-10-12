# Quirrel, the engine's script language: the VM and its libraries (quirrel/), and what the code that uses it links
# (jam's add_quirrel.jam): Dagor::QuirrelHeaders, its headers and settings; Dagor::Quirrel, those with the VM, its module
# system and the engine's Quirrel host
add_subdirectory(quirrel)

add_library(1stPartyLibs.quirrel.headers INTERFACE)
add_library(Dagor::QuirrelHeaders ALIAS 1stPartyLibs.quirrel.headers)
target_include_directories(1stPartyLibs.quirrel.headers INTERFACE
  "${CMAKE_CURRENT_SOURCE_DIR}/quirrel/include"
  "${CMAKE_CURRENT_SOURCE_DIR}/quirrel/sqrat/include"
  "${CMAKE_CURRENT_SOURCE_DIR}/quirrel"
  "${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel/quirrelHost")
target_compile_definitions(1stPartyLibs.quirrel.headers INTERFACE QUIRREL_HOST_HEADER=dagor_quirrel_host.h
  USE_SQRAT_CONFIG "$<$<CONFIG:Rel,IRel>:SQ_STORE_DOC_OBJECTS=0>")

add_library(1stPartyLibs.quirrel INTERFACE)
add_library(Dagor::Quirrel ALIAS 1stPartyLibs.quirrel)
target_link_libraries(1stPartyLibs.quirrel INTERFACE 1stPartyLibs.quirrel.headers 1stPartyLibs.quirrel.quirrel
  1stPartyLibs.quirrel.quirrel.sqmodules gameLibs.quirrel.quirrelHost)
