# The embedded editor (F12, outside Rel builds): it opens over the game and closes again, its daRg UI, the UI fonts and
# the overlay UI script loading without errors. It is mouse-driven, so unlike the scenario tests it has the machine's
# pointing device (hidDriversInit -5: All=7 minus the keyboard and the joysticks).
dagor_add_game_test(starter_game.editor LAYER scenario TAGS starter_game PATHS .
  SCENE ../prog/tests/scenarios/default_world.blk CASE_TIMEOUT 120 ARGS -config:input/hidDriversInit:i=-5)
