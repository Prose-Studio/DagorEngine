# Exercise the installed package and its launcher, including spaces in paths and forwarded arguments.
dagor_add_exec_test(cmake.packaging COMMAND ${Python3_EXECUTABLE} "${CMAKE_CURRENT_SOURCE_DIR}/test_packaging.py"
  "${CMAKE_COMMAND}" TAGS tools)
