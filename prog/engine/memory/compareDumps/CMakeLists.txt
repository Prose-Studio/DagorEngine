# compare_dumps.py, the memory dump differ: its tests
dagor_add_exec_test(engine.memory.compareDumps COMMAND ${Python3_EXECUTABLE} -m unittest -v test_compare_dumps TAGS engine)
