![Python App](https://github.com/SpookyBear0/pygdrpc/workflows/Python%20App/badge.svg)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

# PyGDRPC 1.2.1b
Geometry Dash rich presence, rewritten in Python!
  
![Example](https://i.imgur.com/hoMXIHh.png)
## Features
- Level name and normal mode percentage
- Shows when you are in the editor (No name for security)
- Difficulty faces
- Name and normal mode percentage on local levels
- Shows when you are in menu
 
## How to use
1. Download exe from releases
2. Open Geometry Dash (Note: GDPS don't work)
3. Start `pygdrpc.exe`

## Configuring
PyGDRPC is flexible, and allows you to change multiple options.
It is **not** hard to configure:
* `true` = enable
* `false` = disable

Default configuration should already suit the majority of the people.

## Compiling
If you want to get the latest devoloper version right off the master branch, you can build it yourself.

**Requirements**

- Python >=3.6
- All modules in `src/requirements.txt` (`pip install -r src/requirements.txt`)
- `pyinstaller` module (`pip install pyinstaller`)

### Building
 
1. Clone repo
2. CD to the folder you want to compile from in command prompt.
3. Run the command `python3 -m PyInstaller -F --hiddenimport pkg_resources.py2_warn -i assets/gd.ico src/pygdrpc.py` (if it says command not found - try replacing `python3` with `python` or `py`)
4. Wait for it to finish then go in the newly created folder `dist`, and your file should be waiting there.
 
## Planned Features:
- None at the moment, if you want a feature, make an issue.
 
## Credits:
- Nekit: Showing me how to use the memory part of gd.py and more


**Please tell me if you like this program. Make an issue if you want to suggest features.**
