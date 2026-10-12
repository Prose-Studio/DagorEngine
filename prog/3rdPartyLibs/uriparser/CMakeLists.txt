# uriparser: RFC 3986 URI parsing
dagor_add_target(NAME 3rdPartyLibs.uriparser STATIC LAX
  FILES_CMAKE uriparser_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/uriparser/include ${DAGOR_PROG_DIR}/3rdPartyLibs/uriparser/src
  COMPILE_DEFINITIONS PRIVATE URI_STATIC_BUILD URI_NO_UNICODE
)
