set(defines __B_NO_MEM_BASE_INCLUDE _CRT_SECURE_NO_WARNINGS HAVE_FREETYPE HB_NO_GETENV HB_USE_ATEXIT)
if(WIN32 AND DAGOR_ARCH STREQUAL "x86_64")
  list(APPEND options -wd4267)
endif()
if(CMAKE_SYSTEM_NAME MATCHES "^(Android|Linux)$")
  list(APPEND defines HAVE_PTHREAD)
endif()

dagor_add_target(NAME 3rdPartyLibs.freetype.harfbuzz-2.6.4 STATIC LAX
  FILES_CMAKE harfbuzz-2.6.4_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/freetype/harfbuzz-2.6.4/src
    ${DAGOR_PROG_DIR}/3rdPartyLibs/freetype/freetype-2.8/include
  COMPILE_DEFINITIONS PRIVATE ${defines}
  COMPILE_OPTIONS PRIVATE ${options}
)

# harfbuzz's own test programs: the self-checks, and those that take a font, on the fonts of prog/tools/toolsData
# (test-ot-meta, test-gpos-size-params and test-gsub-would-substitute need a font with a 'meta' table, a 'size' feature
# or a known GSUB lookup, which none of those has; test-buffer-serialize reads stdin)
if(DAGOR_ENGINE_TESTS)
  set(self_checks array bimap number unicode-ranges)
  if(NOT CMAKE_CXX_COMPILER_ID STREQUAL "MSVC") # these do not compile with MSVC (test-meta not as C++20 at all)
    list(APPEND self_checks algs iter)
  endif()
  set(programs "hb_info|main.cc" "hb_test|test.cc")
  foreach(name ot-glyphname ot-name ${self_checks})
    list(APPEND programs "hb_test-${name}|test-${name}.cc")
  endforeach()
  foreach(program IN LISTS programs)
    string(REPLACE "|" ";" program "${program}")
    list(GET program 0 name)
    list(GET program 1 hb_source)
    dagor_add_target(NAME ${name} EXECUTABLE LAX
      FILES_CMAKE hb_test_files.cmake
      INCLUDE_DIRECTORIES PRIVATE src ${DAGOR_PROG_DIR}/3rdPartyLibs/freetype/freetype-2.8/include
      COMPILE_DEFINITIONS PRIVATE ${defines}
      BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.freetype.harfbuzz-2.6.4 3rdPartyLibs.freetype.freetype-2.8
    )
  endforeach()
  foreach(name IN LISTS self_checks)
    dagor_add_exec_test(3rdPartyLibs.harfbuzz.${name} COMMAND $<TARGET_FILE:hb_test-${name}> TAGS 3rdPartyLibs)
  endforeach()
  set(fonts ${DAGOR_PROG_DIR}/tools/toolsData/dargbox/fonts)
  foreach(test "hb_info|NotoSans-Regular.ttf" "hb_test|NotoSans-Regular.ttf" "hb_test-ot-name|NotoSans-Regular.ttf"
               "hb_test-ot-glyphname|lato-regular.ttf") # (Noto Sans has no glyph names)
    string(REPLACE "|" ";" test "${test}")
    list(GET test 0 program)
    list(GET test 1 font)
    dagor_add_exec_test(3rdPartyLibs.harfbuzz.${program} COMMAND $<TARGET_FILE:${program}> ${fonts}/${font}
      TAGS 3rdPartyLibs)
  endforeach()
endif()
