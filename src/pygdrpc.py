from pypresence import Presence
import time
import gd
import asyncio
import os
import json
from termcolor import cprint
import time
from pyfiglet import figlet_format
filedir = '__file__:    ', __file__
filedir = filedir[1].rstrip("gdrpc.py")
cprint(figlet_format("PyGDRPC", font="small"))
def Wait (time, silent=False): # time is in seconds
    time = time * 1000
    string = f"ping 192.0.2.1 -n 1 -w {time}" # ping the local machine
    if silent:
        string = string + " >nul"
    os.system(string)
dict = {
  "version": "1.3.0",
  "editor": {
    "LevelNameVisible": "false"
  },
  
  "logs": {
    "Visible": "true"
  }
}
print(f"\nStarting...")
if os.path.isfile(f"{filedir}config.json") and os.access(f"{filedir}config.json", os.R_OK):
    with open(f"{filedir}config.json") as file:
        data = json.load(file)
else:
    with open(f"{filedir}config.json", "w") as file:  
        json.dump(dict, file, indent=4)
        print("Created conifg file! Please reopen the program to start")
        Wait(5, True)
        exit()

try:
    memory = gd.memory.get_memory()
except RuntimeError:
    print("Run GD first!")
    Wait(5, True)
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

runningstr = "\nRunning!" + " v" + data.get("version")
print(runningstr)

run_once = 0
startingtime = 0

while True:
    memory.reload()
    scenev = memory.get_scene_value()
    scene = memory.get_scene()
    ltypev = memory.get_level_type_value()
    ltype = memory.get_level_type()
    iseditor = memory.is_in_editor()
    name = memory.get_level_name()
    creator = memory.get_level_creator()
    currentattempt = memory.get_attempt()
    objects = str(memory.read_bytes(4, 0x3222D0, 0x168, 0x3A0).as_int())
    
    if scenev == 3 and iseditor == False and ltypev == 3:
        if run_once == 0:
            startingtime = int(time.time())
            run_once = 1
        lid = memory.get_level_id()
        smallimage = asyncio.run(get_difficulty(lid))
        if memory.is_practice_mode():
            RPC.update(pid=memory.process_id, state=str(f"{name} by {creator} (Attempt {currentattempt})"), details="Playing a level in practice mode", large_image="gd", small_image=asyncio.run(get_difficulty(lid)), large_text="Geometry Dash", start=startingtime)
        else:
            RPC.update(pid=memory.process_id, state=str(f"{name} by {creator} (Attempt {currentattempt})"), details="Playing a level", large_image="gd", small_image=asyncio.run(get_difficulty(lid)), large_text="Geometry Dash", start=startingtime)
    
    if scenev == 3 and iseditor:
        if run_once == 0:
            startingtime = int(time.time())
            run_once = 1
        if not data.get("editor").get("LevelNameVisible") == "true": RPC.update(pid=memory.process_id, details="Editing a level", state="Details hidden", large_image="gd", small_image="cp", large_text="Geometry Dash", start=startingtime)
        else: RPC.update(pid=memory.process_id, state=str(f"{memory.get_editor_level_name()} ({objects} objects)"), details="Editing a level", large_image="gd", small_image="cp", large_text="Geometry Dash", start=startingtime)
    
    if scenev == 3 and iseditor == False and ltypev == 2:
        if run_once == 0:
            startingtime = int(time.time())
            run_once = 1
        if not data.get("editor").get("LevelNameVisible") == "true":
            if memory.is_practice_mode():
                RPC.update(pid=memory.process_id, state="Details hidden", details="Playing an editor level in practice mode", large_image="gd", small_image="cp", large_text="Geometry Dash", start=startingtime)
            else:
                RPC.update(pid=memory.process_id, state="Details hidden", details="Playing an editor level", large_image="gd", small_image="cp", large_text="Geometry Dash", start=startingtime)
        else:
            if memory.is_practice_mode():
                RPC.update(pid=memory.process_id, state=str(f"{name} (Attempt {currentattempt})"), details="Playing an editor level in practice mode", large_image="gd", small_image="cp", large_text="Geometry Dash", start=startingtime)
            else:
                RPC.update(pid=memory.process_id, state=str(f"{name} (Attempt {currentattempt})"), details="Playing an editor level", large_image="gd", small_image="cp", large_text="Geometry Dash", start=startingtime)
    
    else:
        if ltypev == 0 and scenev != 3:
            run_once = 0
            RPC.update(pid=memory.process_id, state="     ", details="In menu", large_image="gd", large_text="Geometry Dash")
        else:
            if scenev == 9 and ltypev == 1:
                lid = memory.get_level_id()
                olevel = gd.Level.official(lid)
                name = olevel.name
                smallimage = asyncio.run(get_offical_difficulty(lid))
                if run_once == 0:
                    startingtime = int(time.time())
                    run_once = 1
                if memory.is_practice_mode():
                    RPC.update(pid=memory.process_id, state=f"{name} (Attempt {currentattempt})", details="Playing an official level in practice mode", large_image="gd", small_image=smallimage, large_text="Geometry Dash", start=startingtime)
                else:
                    RPC.update(pid=memory.process_id, state=f"{name} (Attempt {currentattempt})", details="Playing an official level", large_image="gd", small_image=smallimage, large_text="Geometry Dash", start=startingtime)
    time.sleep(1)