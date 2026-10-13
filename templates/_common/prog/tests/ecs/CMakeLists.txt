# ECS tests: [ecs_test] functions in *.das here, run by the game with every game system (in a multiplayer game by the
# dedicated server, in a single-player one by the game itself, headless where it can)
dagor_add_game_test(starter_game.ecs LAYER ecs TAGS starter_game PATHS . SCENE gamedata/scenes/main.blk CASE_TIMEOUT 60)
