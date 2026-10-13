# Duktape 2.2.1, the embeddable ECMAScript engine, built as its command line interpreter (duktape)
if(CMAKE_SYSTEM_NAME MATCHES "^(Darwin|Linux)$")
  list(APPEND options -fno-fast-math -Wno-format-overflow)
endif()

dagor_add_target(NAME duktape EXECUTABLE LAX NO_CONFIG_POSTFIX
  FILES_CMAKE duktape_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    examples/cmdline src extras/print-alert extras/console extras/logging extras/module-duktape
  COMPILE_DEFINITIONS PRIVATE
    __B_NO_MEM_BASE_INCLUDE DUK_CMDLINE_PRINTALERT_SUPPORT DUK_CMDLINE_CONSOLE_SUPPORT DUK_CMDLINE_LOGGING_SUPPORT
    DUK_CMDLINE_MODULE_SUPPORT DUK_CMDLINE_FILEIO
  COMPILE_OPTIONS PRIVATE ${options}
  CDK
)
