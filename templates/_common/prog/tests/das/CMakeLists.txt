# daScript unit tests: pure logic of the game scripts, run by dastest without the game, in this dir (tests.das_project
# finds the game's scripts relative to it)
dagor_add_das_test(starter_game.das TAGS starter_game PATHS . PROJECT tests.das_project WORKING_DIRECTORY .)
