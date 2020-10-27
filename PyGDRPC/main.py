import pypresence
import gd
import asyncio
from config import config
import os
from time import sleep, time
from gd.enums import *
from helpers import get_difficulty

client = gd.Client()
client_id = "703049428822655048"

try:
    memory = gd.memory.get_state(load=True)
except LookupError:
    print("Run GD first!")
    os.system("PAUSE")
    exit()

pid = memory.process_id
startingtime = int(time())
game_manager = memory.get_game_manager()
editor_layer = game_manager.get_editor_layer()
play_layer = game_manager.get_play_layer()
player = play_layer.get_player()
level = play_layer.get_level_settings().get_level()
account_manager = memory.get_account_manager()
user_name = account_manager.get_user_name()

def exit():
    os._exit(0)

async def main():
    while True:
        scene = game_manager.get_scene()
        if scene == Scene.EDITOR_OR_LEVEL:
            if not editor_layer.is_null():
                object_count=editor_layer.get_object_count()
                editor_level = editor_layer.get_level_settings().get_level()
                editorlevelname = editor_level.get_name()

                if not config["editor"]["levelnamevisible"]: 
                    await rpc.update(pid=pid, details="Editing a level", 
                    state="Details hidden", 
                    large_image="gd", 
                    small_image="cp", 
                    large_text="Geometry Dash", 
                    start=startingtime)
                else: 
                    await rpc.update(pid=pid, details="Editing a level", 
                    state=f"{editorlevelname} ({object_count} objects)", 
                    large_image="gd", 
                    small_image="cp", 
                    large_text="Geometry Dash", 
                    start=startingtime)
            elif editor_layer.is_null() and level.get_level_type() == LevelType.EDITOR:
                attempt = play_layer.get_attempt()
                levelid = level.get_id()
                name = level.get_name()
                creator = level.get_creator_name()
                if config["editor"]["levelnamevisible"]:
                    await rpc.update(pid=pid, state=str(f"{name} (Attempt {attempt})"), 
                    details="Playing an editor level", 
                    large_image="gd", 
                    small_image="cp", 
                    large_text="Geometry Dash", 
                    start=startingtime)
                else:
                    await rpc.update(pid=pid, state=str(f"{name} by {creator} (Attempt {attempt})"), 
                    details="Playing a level", 
                    large_image="gd", 
                    small_image=await get_difficulty(levelid), 
                    large_text="Geometry Dash", 
                    start=startingtime)
            else:
                await rpc.update(pid=pid, state="Details hidden", 
                details="Playing an editor level", 
                large_image="gd", 
                small_image="cp", 
                large_text="Geometry Dash", 
                start=startingtime)
        sleep(1)
    

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    rpc = pypresence.AioPresence(client_id)
    rpc.loop.run_until_complete(rpc.connect())
    try:
        rpc.loop.run_forever()
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()
        exit()