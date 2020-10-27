import gd

client = gd.Client
levelid = gd.memory.get_memory().get_level_id()

async def get_difficulty(level: gd.Level) -> str:
    try:
        level = await client.get_level(levelid)
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