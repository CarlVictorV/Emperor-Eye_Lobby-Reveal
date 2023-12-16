# RiotWatcher-LCU-RiotClient-API-Practice

Testing RiotWatchers-LCU-RiotClient-API

# Requirements

- Submit a record of the demonstration of your application.

- Submit a PDF document containing documentation about your system. Follow the same formatting used from your previous WebDev2 subject. Make sure that you highlight the problem you're trying to solve/solution you're trying to improve.

- Submit a link to your github repositories and with proper readme.md files for me to test and replicate your system.

# Documentation

- Asked from a friend who was taking webdev2 at the time. He gave me a copy of this documentation. I don't know if this is what the professor wanted but this is what I got.
- https://docs.google.com/document/d/1rdwhAMr4NXFnXc8S1wLS2ELAhm_mEkydcTq4cKp9nNQ/edit#heading=h.dywidl7odf4x

# Imports

- lcu_driver
- requests
- riotwatcher
- json
- platform
- psutil
- base64
- warnings

# Hardest Part :skull:

- Download Riot Client :skull:
- Download League of Legends :skull:

# Documentation of RiotWatcher

- https://riot-watcher.readthedocs.io/en/latest/riotwatcher/LeagueOfLegends/index.html
- This assumes you have a valid API key
- This is basically a wrapper for the Riot API
- https://developer.riotgames.com/apis
- Technially this is not needed but this would have been a good feature to use and not rely on other websites to get the data. Like OP.GG or etc.

# Documentation of LCU_Driver (Important)

- https://swagger.dysolix.dev/lcu/#/
- The important part is simply /lol-champ-select/v1/session as it is the only way to know if you are in a champ select or not
- Other than that there might be other use for the LCU. 

# Documentation of Riot Client (Important)

- https://riotclient.kebs.dev/#operation--GET%20/chat/v5/participants
- The important part is simply /chat/v5/participants as it is the only way to see who is in your lobby hidden or not

# Testing

- To test if the program is working you can simply play a game of League of Legends
- Specifically try Custom Games, Co-op vs AI, and of course it's main purpose Ranked Solo/Duo (advisable to use a smurf account unless you want to lose LP)

# How to Use

- Play a game of League of Legends (Ranked Solo/Duo)
- Run the program (before or during champ select)
- Program will show you who is in your lobby
- Program will also give out links to OP.GG for each player in your lobby

# Important Notes

- You really need to have the Riot Client open for this to work
- You technically don't need to have League of Legends open for this to work, this could be used for Valorant or TFT or etc. Though again the program is called League of Legends so it would be weird to use it for other games.

# HOW TO GET API KEY FROM RIOT

- https://developer.riotgames.com/
- Go to this website and login with your Riot Account
- Paste the API key in the API_KEY variable in the program
