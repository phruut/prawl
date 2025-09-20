gold and exp farming timer script for **brawlhalla patch 9.12**\
help/dev discord server: https://discord.gg/2HDmuqqq9p  
video tutorial (old version): https://youtu.be/SWuSntfHioQ

<img width="277" height="162" alt="prawl-0 1 2" src="https://github.com/user-attachments/assets/54e57536-92c7-47cb-8fcb-43ab7b868dcd" />

## 💡important
add this steam startup option
```
-noeac
```
> [!caution]
> please **always** use `-noeac` launch option to avoid the risk of any bans, although it is highly unlikely\
> _i am not responsible for anything that happens to your account_

## 🔥features
- launch brawlhalla from gui (+auto launch on script start option)
- set custom values and adjust timings
- auto start matches, also configurable
- show/hide brawlhalla window
- runs in the background (no interruption as it directly sends inputs to the brawlhalla window only)
- gold/exp rate limit detection (starts again after waiting for the rate limit to reset)
- super light weight and minimal dependencies as its basically just a timer script
- check for update button

_please see the [wiki](https://github.com/phruut/prawl/wiki) for more information about the script_

### other
- [ ] pixel search mode?
- [ ] fix input bugs(?) laptop has issues idk why
- [ ] memory read mode (ehhhh)
- [ ] legends / user data (exp, gold, time spent, etc)
- [ ] dynamic ui scaling (maaaybe)

## 🔎download
you can find the (old) compiled script in the [releases page](https://github.com/phruut/prawl/releases), or [click here to download](https://github.com/phruut/prawl/releases/download/241209/farm_1209.exe)
> [!warning]
> your anti-virus may flag this executable as a threat, as it interacts with Win32 API for sending key inputs and cmd for launching brawlhalla

## 🚀manual install
```bash
git clone https://github.com/phruut/prawl
```
```bash
cd prawl
```
```Pip Requirements
python -m pip install -r requirements.txt
```
and then you can run it
```bash
python main.py
```

## compiled with nuitka
```bash
nuitka --onefile --windows-console-mode=disable --windows-icon-from-ico=res\praw-app.ico main.py
```

## 🔗links
- [Piconic font](https://www.pentacom.jp/pentacom/bitfontmaker2/gallery/?id=9261) - icons font
- [cq-pixel font](https://github.com/cpuQ) -  main ui font
- [Dear PyGui](https://github.com/hoffstadt/DearPyGui) - gui library
- [pywin32](https://github.com/mhammond/pywin32) - win32 api things
- [py-window-styles](https://github.com/Akascape/py-window-styles) - window stuff
- [Nuitka](https://github.com/Nuitka/Nuitka) - compiler
