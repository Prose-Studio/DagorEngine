# Duktape 2.2.1, the embeddable ECMAScript engine, built as its command line interpreter (duktape)
set(includes examples/cmdline src)
set(defines __B_NO_MEM_BASE_INCLUDE)
list(APPEND defines DUK_CMDLINE_PRINTALERT_SUPPORT)
list(APPEND includes extras/print-alert)
list(APPEND defines DUK_CMDLINE_CONSOLE_SUPPORT)
list(APPEND includes extras/console)
list(APPEND defines DUK_CMDLINE_LOGGING_SUPPORT)
list(APPEND includes extras/logging)
list(APPEND defines DUK_CMDLINE_MODULE_SUPPORT)
list(APPEND includes extras/module-duktape)
list(APPEND defines DUK_CMDLINE_FILEIO)
if(CMAKE_SYSTEM_NAME MATCHES "^(Darwin|Linux)$")
  list(APPEND options -fno-fast-math -Wno-format-overflow)
endif()

dagor_add_target(NAME duktape EXECUTABLE LAX NO_CONFIG_POSTFIX
  FILES_CMAKE duktape_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE ${defines}
  COMPILE_OPTIONS PRIVATE ${options}
  CDK
)
