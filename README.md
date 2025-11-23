# CS2-Yahiamod
## A fun little port of Yahiamod for Counter Strike 2 using Counter Strike 2 Gamestate Intergration

## **The youtube video isnt made yet** , im just lazy and dont want to update it later.

> [!CAUTION]
> This mod is unstable at this point in time , and as such is in a "beta" phase as i add features and try to make the experience better.
> All releases are stable versions , downloading directly from the current git is a risk you are accepting.

> [!NOTE]
> This mod may increase lag as it works with CS:GSI over the network, trying to have real-time actions uses bandwidth.
> Additionally , the Server py i use to gather data from the CS app uses a decent chunk of the CPU. Sorry.

# SETUP 

This is a **Python only project**, so python HAS to be installed.
You also **need PIP for the extra packages** , pip can be found on its native website.

> [!NOTE]
> This mod requires python 3.12

Next , **you need to install all the Packages that Python needs** to run this project:
1) open a terminal window (search "terminal" or "cd")
2) Paste this command:
```
   py -m pip install tk pillow pynput pygame flask pyautogui winregistry vdf
```
<details>

**<summary>Worried this is a malicious command? Click here for an explanation</summary>**

Python packages are libraries for python to use , and are usually built in. yahiamod uses a lot of built in ones but some things are very neiche so need further specific packages. Heres what each one is:

- tk - Also known as TKinter , this is the library i use to make the overlays and visual effects
- pillow - Used to pre-load images to improve performance.
- pygame - A package used to make games in python, handy to play audio with!
- flask - Used by server.py to listen out for the CS GSI!
- winregistry - reading windows registries to find where Steam is located.
- vdf - Used for reading Valve (steam) files.

</details>

> [!IMPORTANT]
> If the program crashes , it is likely one of these is missing!


> [!NOTE]
> This next step is automated with the latest experimental release.

Next you need to place the configuration file that Yahiamod uses to communicate with Counter strike.
Inside the project folder you will find "gamestate_integration_yahamouse" , this is the config file!
This needs to go into your Counter strike CFG directory. It should look like:

```
"SteamLibrary\steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg"
```

Place "gamestate_integration_yahamouse.cfg" into this folder. 

> [!WARNING]
> if you have cs:go legacy installed , you might have multiple folders named cfg , try to follow this exact path.

Thats all for the setup!

# Features
While this script is supposed to be a direct port of Yahiamod for Balatro , i have taken some other memes aswell that better fit CS2.
All features here are (mostly) spoiler free. For a deeper look on these features , check the youtube video.

**That one french tiktoker with that hell of a dumpy** - He kindly reminds you if you need more bullets.

**Mucho Texto** - Anti-spam chat feature 
> [!CAUTION]
> This feature can fire when outside of Counter Strike

**21 kid** - 21 kid helpfully reminds you when you have 9 , 10 or 21 bullets left.

**Lobotomy** - you didnt die , your just sobering up from your lobotomy... sometimes you get that feeling you should be playing balatro..

**Cantaloupe** - Your struggling to convince your spouse to elope with you.. maybe some kills would change their mind.

**Tasty as hell** - You have grown a strange fondness to the taste of your burnt uniform , makes you want to sing how good it is. 

**Fishy friend** - If you die too much , your fishy friend comes in to help :]

**Moroccan internet** - (this feature is complicated. want a full breakdown? check the video on my channel.) If your ping-meter goes to high , your are forcibly removed and shipped to morocco.

**Important video** - If you stand infront of your computer and open main.py 50 times , some say you will get an important video...

**Lemur** - Think fast chucklenuts!

**DR whatsapp** - You get a paper cut and lose some health , so you whatsapp your doctor for help.

**HIT UP THE SLOTS** - If you gain or lose a significant amount of money , you are sent to gamble.

**Yahiassistance** - Everybody knows getting assists is way worse than getting kills , so if you get too many assists , Yahiamice assists you with his encouraging voice.
