gold and exp farming timer script for **brawlhalla patch 9.12**\
please see the [wiki](https://github.com/phruut/prawl/wiki) for more information about the script\
help/dev server: https://discord.gg/2HDmuqqq9p  
video tutorial: https://youtu.be/SWuSntfHioQ

## 💡important
add this steam startup option
```
-noeac
```
> [!caution]
> please **always** use `-noeac` option before using the script to avoid the risk of any bans, although it is highly unlikely\
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

### other
- [ ] pixel search mode?
- [ ] fix input bugs(?) laptop has issues idk why
- [ ] memory read mode
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
- [Nuitka](https://github.com/Nuitka/Nuitka) - compiler
