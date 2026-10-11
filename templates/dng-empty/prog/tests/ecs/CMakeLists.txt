# ECS tests: [ecs_test] functions in *.das here, run by the dedicated server with every game system
dagor_add_game_test(dng_empty.ecs LAYER ecs TAGS dng_empty PATHS . SCENE gamedata/scenes/main.blk CASE_TIMEOUT 60)
