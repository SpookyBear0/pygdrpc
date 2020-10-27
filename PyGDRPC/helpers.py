import gd

client = gd.Client()
memory = gd.memory.get_state(load=True)
game_manager = memory.get_game_manager()
play_layer = game_manager.get_play_layer()
level = play_layer.get_level_settings().get_level()
levelid = level.get_id()

async def get_difficulty(level: gd.Level) -> str:
    try:
        level = await client.get_level(level_id=levelid)
    except gd.MissingAccess:
        pass
    else:
        base = level.difficulty.name.lower().split("_")
        if level.is_epic():
            base.append("epic")
        elif level.is_featured():
            base.append("featured")
        return '-'.join(base)

async def get_offical_difficulty(level: gd.Level) -> str:
    try:
        olevel = gd.Level.official(levelid)
    except gd.MissingAccess:
        pass
    else:
        base = olevel.difficulty.name.lower().split("_")
        return '-'.join(base)