gold and xp farming bot, afk farmer, macro, script, any legend, all legends, windows\
tested and working for **brawlhalla patch 10.01**\
help/dev discord server: https://discord.gg/2HDmuqqq9p  
video tutorial (old version): https://youtu.be/SWuSntfHioQ

<img width="277" height="162" alt="prawl-0 1 2" src="https://github.com/user-attachments/assets/54e57536-92c7-47cb-8fcb-43ab7b868dcd" />

## 💡 important
add this steam startup option
```
-noeac
```
> [!caution]
> please **always** use `-noeac` launch option to avoid the risk of any bans, although it is highly unlikely\
> _i am not responsible for anything that happens to your account_

## 🔥 features
- launch brawlhalla from gui (+auto launch on script start option)
- set custom values and adjust timings
- auto start matches, also configurable
- show/hide brawlhalla window
- runs in the background (no interruption as it directly sends inputs to the brawlhalla window only)
- gold/exp rate limit detection (starts again after waiting for the rate limit to reset)
- super light weight and minimal dependencies as its basically just a timer script
- check for update button

_please see the [wiki](https://github.com/phruut/prawl/wiki) for more information about the script_

## 😭 todo

main
- [ ] python installation video asdkjhgakshgasgs
- [ ] finish adding logging
- [ ] check for updates on server host info directly from this repository

qol?
- [ ] starting mid match?
- [ ] in disconnect net, if it fails the first time, reduce the timer by the amount of time waited.
- [ ] legends / user data (exp, gold, time spent, etc)
- [ ] headless mode?

soon
- [ ] update slider text based on set_value commands too
- [ ] automatic colors based on windows theme accent color
- [ ] setting profiles
- [ ] customizable themes page, basically have 3-4 main colors, and adjust or give variations to them


## 🔎 download
you can find the (old) compiled farm.py in the [releases page](https://github.com/phruut/prawl/releases), or [click here to download](https://github.com/phruut/prawl/releases/download/241209/farm_1209.exe)
> [!warning]
> your anti-virus may flag this executable as a threat, as it interacts with Win32 API for sending key inputs and cmd for launching brawlhalla

## 🚀 manual install
```bash
# clone repo and install dependencies
git clone https://github.com/phruut/prawl
cd prawl
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt

# and then you can run it
python main.py
```

## 🔗 links
- [Piconic font](https://www.pentacom.jp/pentacom/bitfontmaker2/gallery/?id=9261) - icons font
- [cq-pixel font](https://github.com/cpuQ) -  main ui font
- [Dear PyGui](https://github.com/hoffstadt/DearPyGui) - gui library
- [pywin32](https://github.com/mhammond/pywin32) - win32 api things
- [py-window-styles](https://github.com/Akascape/py-window-styles) - window stuff
- [Nuitka](https://github.com/Nuitka/Nuitka) - compiler
