from pypresence import Presence
import time
import gd
import asyncio
import os
import json
from termcolor import cprint
from pyfiglet import figlet_format
filedir = '__file__:    ', __file__
filedir = filedir[1].rstrip("gdrpc.py")
cprint(figlet_format("PyGDRPC", font="small"))
print(f"\nStarting...")
with open(f"{filedir}config.json") as file:
    data = json.load(file)

def Wait (time, silent=False): # time is in seconds
    time = time * 1000
    string = f"ping 192.0.2.1 -n 1 -w {time}" # ping the local machine
    if silent:
        string = string + " >nul"
    os.system(string)

try:
    memory = gd.memory.get_memory()
except RuntimeError:
    print("Run GD first!")
    Wait(10, True)
    exit()

smallimage = "none" # fallback in case of the difficulty face not being returned
client = gd.Client()
editorlevel = False
client_id = "703049428822655048"
RPC = Presence(client_id)
if data.get("logs") == "Visible": print("Connecting...")
RPC.connect()

async def get_difficulty(level: gd.Level) -> str:
    try:
        level = await client.get_level(lid)
    except gd.MissingAccess:
        editorlevel = True
    else:
        editorlevel = False
        base = level.difficulty.name.lower().split("_")
        if level.is_epic():
            base.append("epic")
        elif level.is_featured():
            base.append("featured")
        return '-'.join(base)

async def get_offical_difficulty(level: gd.Level) -> str:
    global editorlevel
    try:
        olevel = gd.Level.official(lid)
    except gd.MissingAccess:
        editorlevel = True
    else:
        editorlevel = False
        base = olevel.difficulty.name.lower().split("_")
        return '-'.join(base)

runningstr = "\nRunning!"
if data.get("logs").get("Visible") == True: runningstr = runningstr + " v" + data.get("version")
print(runningstr)

while True:
    memory.reload()
    scenev = memory.get_scene_value()
    scene = memory.get_scene()
    ltypev = memory.get_level_type_value()
    ltype = memory.get_level_type()
    iseditor = memory.is_in_editor()
    name = memory.get_level_name()
    percent = str(memory.get_normal_percent())
    objects = str(memory.read_bytes(4, 0x3222D0, 0x168, 0x3A0).as_int())
    
    if scenev == 3 and iseditor == False and ltypev == 3:
        lid = memory.get_level_id()
        smallimage = asyncio.run(get_difficulty(lid))
        RPC.update(pid=memory.process_id, state=str(f"{name} ({percent}%)"), details="Playing a level", large_image="gd", small_image=asyncio.run(get_difficulty(lid)), large_text="Geometry Dash")
    
    if scenev == 3 and iseditor:
        if not data.get("editor").get("LevelNameVisible") == True: RPC.update(pid=memory.process_id, details="Editing a level", large_image="gd", small_image="cp", large_text="Geometry Dash")
        else: RPC.update(pid=memory.process_id, state=str(f"{name} ({objects} objects)"), details="Editing a level", large_image="gd", small_image="cp", large_text="Geometry Dash")
    
    if scenev == 3 and iseditor == False and ltypev == 2:
        if not data.get("editor").get("LevelNameVisible") == True: RPC.update(pid=memory.process_id, state=str(f"({percent}%)"), details="Playing an editor level", large_image="gd", small_image="cp", large_text="Geometry Dash")
        else: RPC.update(pid=memory.process_id, state=str(f"{name} ({percent}%)"), details="Playing an editor level", large_image="gd", small_image="cp", large_text="Geometry Dash")
    
    else:
        if ltypev == 0 and scenev != 3:
            RPC.update(pid=memory.process_id, state="     ", details="In menu", large_image="gd", large_text="Geometry Dash")
        else:
            if scenev == 9 and ltypev == 1:
                lid = memory.get_level_id()
                olevel = gd.Level.official(lid)
                name = olevel.name
                smallimage = asyncio.run(get_offical_difficulty(lid))
                RPC.update(pid=memory.process_id, state=f"{name} ({percent}%)", details="Playing an official level", large_image="gd", small_image=smallimage, large_text="Geometry Dash")
    time.sleep(5)
