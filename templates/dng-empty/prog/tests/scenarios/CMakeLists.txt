# Scenario tests: the client renders, the tests drive it and compare screenshots with references/ (needs the game's
# shaders: cmake --build --preset <host>-client-content)
dagor_add_game_test(dng_empty.scenarios LAYER scenario TAGS dng_empty PATHS .
  SCENE ../prog/tests/scenarios/default_world.blk CASE_TIMEOUT 120)
