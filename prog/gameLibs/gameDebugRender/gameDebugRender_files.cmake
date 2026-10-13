set(FILES
  primitivesCache.cpp
  primitives2dCache.cpp
  primitivesRender.cpp
  crosshairPrimitive.cpp
  textRender.cpp
)
if(DAGOR_DEDICATED)
  list(APPEND FILES debugDrawStub.cpp)
else()
  list(APPEND FILES "$<IF:$<CONFIG:Rel>,${CMAKE_CURRENT_LIST_DIR}/debugDrawStub.cpp,${CMAKE_CURRENT_LIST_DIR}/debugDraw.cpp>")
endif()
