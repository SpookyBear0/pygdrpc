import pypresence
import gd
import asyncio
from config import config
import os
from time import sleep, time
from helpers import get_difficulty

client = gd.Client()
client_id = "703049428822655048"

try:
    memory = gd.memory.get_memory()
except RuntimeError:
    print("Run GD first!")
    os.system("PAUSE")
    exit()

pid = memory.process_id
startingtime = int(time())
scenevalue = memory.get_scene_value()
scene = memory.get_scene()
leveltypevalue = memory.get_level_type_value()
leveltype = memory.get_level_type()
iseditor = memory.is_in_editor()
name = memory.get_level_name()
creator = memory.get_level_creator()
currentattempt = memory.get_attempt()
ispractice = memory.is_practice_mode()
editorlevelname = memory.get_editor_level_name()
levelid = memory.get_level_id()
objects = str(memory.read_bytes(4, 0x3222D0, 0x168, 0x3A0).as_int())

def exit():
    os._exit(0)

async def main():
    while True:
        if scenevalue == 3 and iseditor:
            print(1)
            if not config["editor"]["levelnamevisible"]: await rpc.update(pid=pid, details="Editing a level", 
            state="Details hidden", 
            large_image="gd", 
            small_image="cp", 
            large_text="Geometry Dash", 
            start=startingtime)
            else: await rpc.update(pid=pid, details="Editing a level", 
            state=f"{editorlevelname} ({objects} objects)", 
            large_image="gd", 
            small_image="cp", 
            large_text="Geometry Dash", 
            start=startingtime)


        if scenevalue == 3 and leveltypevalue == 3:
            print(2)
            if ispractice:
                await rpc.update(pid=pid, state=str(f"{name} by {creator} (Attempt {currentattempt})"), 
                details="Playing a level in practice mode", 
                large_image="gd", 
                small_image=await get_difficulty(levelid), 
                large_text="Geometry Dash", 
                start=startingtime)
            else:
                await rpc.update(pid=pid, state=str(f"{name} by {creator} (Attempt {currentattempt})"), 
                details="Playing a level", 
                large_image="gd", 
                small_image=await get_difficulty(levelid), 
                large_text="Geometry Dash", 
                start=startingtime)

        if scenevalue == 3 and iseditor == False and leveltypevalue == 2:
            print(3)
            if ispractice:
                practice = " in practice mode"
            else:
                practice = ""
            if config["editor"]["levelnamevisible"]:
                await rpc.update(pid=pid, state=str(f"{name} (Attempt {currentattempt})"), 
                details="Playing an editor level" + practice, 
                large_image="gd", 
                small_image="cp", 
                large_text="Geometry Dash", 
                start=startingtime)
            else:
                await rpc.update(pid=pid, state="Details hidden", 
                details="Playing an editor level" + practice, 
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