import json
import os
from time import sleep

dir_path = os.path.dirname(os.path.realpath(__file__))

default_config = {
    "version": "1.0.0",
    "editor": {
        "levelnamevisible": False
    }
}

if os.path.exists(f"{dir_path}/config.json"):
    with open(f"{dir_path}/config.json") as file:
        config = json.load(file)
else:
    with open(f"{dir_path}/config.json", "w") as file:  
        json.dump(default_config, file)
        print("Created conifg file! Please reopen the program to start")
        os.system("PAUSE")