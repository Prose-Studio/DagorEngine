# Scenario tests: the client renders, the tests drive it and compare screenshots with references/ (needs the game's
# shaders: cmake --build --preset <host>-client-content)
dagor_add_game_test(starter_game.scenarios LAYER scenario TAGS starter_game PATHS .
  SCENE ../prog/tests/scenarios/default_world.blk CASE_TIMEOUT 120)
