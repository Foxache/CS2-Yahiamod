# CS2-Yahiamod
A fun little port of Yahiamod for Counter Strike 2 using Counter Strike 2 Gamestate Intergration

# This mod is **HIGHLY unstable** at this point in time , and as such is in a "beta" phase as i add features and try to make the experience better.

# This mod is **HIGHLY CPU intensive!** It maxes out my weasly overclocked 6600k. Want to know why? Check the youtube video.

# **The youtube video isnt made yet** , im just lazy and dont want to update it later.

# SETUP 

More detail inside the readme. This setup is also availiable as a video on my Youtube Channel DingusDongulus

This is a Python only project, so python HAS to be installed.
You also need PIP for the extra packages , pip can be found on its native website.

Next , you need to install all the Packages that Python needs to run this project:
1) open a terminal window (search "terminal")
2) Paste this command:

   py -m pip install tk opencv-python pillow pynput pygame flask pyautogui rich

   
If the project opens , but swiftly closes , you are probably missing one of these!

Next you need to place the configuration file that Yahiamod uses to communicate with Counter strike.
Inside the project folder you will find "gamestate_integration_yahamouse" , this is the config file!
This needs to go into your Counter strike CFG directory. It should look like:

"SteamLibrary\steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg"

Place "gamestate_integration_yahamouse.cfg" into this folder. 

*if you have cs:go legacy installed , you might have multiple folders named cfg , try to go for ones closest to this directory.*

Lastly , you need to change you STEAMID in the main.py script.
This is quite simple , open the main.py with Notepad , and replace the id in line 15 with your Steamid64 
How do you get your steam id?
It is this part of your steam profile link:

https://steamcommunity.com/profiles/ *4656121292394910* /

If you havent done this correctly , the code will shout at you to change it.

Thats all for the setup!

# Features
While this script is supposed to be a direct port of Yahiamod for Balatro , i have taken some other memes aswell that better fit CS2.
All features here are (mostly) spoiler free. For a deeper look on these features , check the youtube video.

**That one french tiktoker with that hell of a dumpy** - He kindly reminds you if you need more bullets.

**Mucho Texto** - Anti-spam chat feature *this feature does not just affect CS2

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
