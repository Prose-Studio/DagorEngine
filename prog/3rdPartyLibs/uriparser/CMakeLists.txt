# uriparser: RFC 3986 URI parsing
set(sources
  src/UriCommon.c
  src/UriCompare.c
  src/UriEscape.c
  src/UriFile.c
  src/UriIp4Base.c
  src/UriIp4.c
  src/UriMemory.c
  src/UriNormalizeBase.c
  src/UriNormalize.c
  src/UriParseBase.c
  src/UriParse.c
  src/UriQuery.c
  src/UriRecompose.c
  src/UriResolve.c
  src/UriShorten.c
)
set(includes ${DAGOR_PROG_DIR}/3rdPartyLibs/uriparser/include ${DAGOR_PROG_DIR}/3rdPartyLibs/uriparser/src)
list(APPEND defines URI_STATIC_BUILD URI_NO_UNICODE)

dagor_add_library(3rdPartyLibs.uriparser LAX ${sources})
target_include_directories(3rdPartyLibs.uriparser PRIVATE ${includes})
target_compile_definitions(3rdPartyLibs.uriparser PRIVATE ${defines})
