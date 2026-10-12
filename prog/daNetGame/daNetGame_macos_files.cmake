# the client's main; the game runs from its dir, where its app bundle is (dagor_apple_bundle):
# <name>.app/Contents/MacOS/../../..
if(NOT DAGOR_DEDICATED)
  set(FILES main/apple_main.mm)
  set_property(SOURCE main/apple_main.mm PROPERTY COMPILE_DEFINITIONS "DAGOR_MACOSX_CONTENTS=\"../../..\"")
endif()
