# Quirrel, the engine's script language: the VM and its libraries (quirrel/), and what the code that uses it links
# (jam's add_quirrel.jam): Dagor::QuirrelHeaders, its headers and settings; Dagor::Quirrel, those with the VM, its module
# system and the engine's Quirrel host
dagor_add_target(NAME 1stPartyLibs.quirrel.headers HEADERONLY
  INCLUDE_DIRECTORIES INTERFACE
    quirrel/include quirrel/sqrat/include quirrel ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel/quirrelHost
  COMPILE_DEFINITIONS INTERFACE
    QUIRREL_HOST_HEADER=dagor_quirrel_host.h USE_SQRAT_CONFIG "$<$<CONFIG:Rel,IRel>:SQ_STORE_DOC_OBJECTS=0>"
  LICENSES quirrel
)
add_library(Dagor::QuirrelHeaders ALIAS 1stPartyLibs.quirrel.headers)

dagor_add_target(NAME 1stPartyLibs.quirrel HEADERONLY
  BUILD_DEPENDENCIES INTERFACE
    1stPartyLibs.quirrel.headers 1stPartyLibs.quirrel.quirrel 1stPartyLibs.quirrel.quirrel.sqmodules
    gameLibs.quirrel.quirrelHost
  LICENSES quirrel
)
add_library(Dagor::Quirrel ALIAS 1stPartyLibs.quirrel)
