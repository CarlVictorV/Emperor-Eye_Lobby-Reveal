import sys
import requests
import json
import platform
import psutil
import base64
from os import system, name
from linkmaker import multi_search
from lcu_driver import Connector
from riotwatcher import LolWatcher, ApiError
import warnings
warnings.filterwarnings('ignore')
# global variables

# Needs to be updated every 24 hours
api_key = 'RGAPI-4ace66ee-3d92-4503-907a-08d8eb284ef7'
watcher = LolWatcher(api_key)
my_region = 'ph2'

app_port = None
auth_token = None
riotclient_auth_token = None
riotclient_app_port = None
region = None
lcu_name = None   # LeagueClientUx executable name
showNotInChampSelect = True
# functions


def getLCUName():
    '''
    Get LeagueClient executable name depending on platform.
    '''
    global lcu_name
    if platform.system() == 'Windows':
        lcu_name = 'LeagueClientUx.exe'
    elif platform.system() == 'Darwin':
        lcu_name = 'LeagueClientUx'
    elif platform.system() == 'Linux':
        lcu_name = 'LeagueClientUx'


def LCUAvailable():
    '''
    Check whether a client is available.
    '''
    return lcu_name in (p.name() for p in psutil.process_iter())


def getLCUArguments():
    global auth_token, app_port, region, riotclient_auth_token, riotclient_app_port
    '''
    Get region, remoting-auth-token and app-port for LeagueClientUx.
    '''
    if not LCUAvailable():
        sys.exit('No ' + lcu_name + ' found. Login to an account and try again.')

    for p in psutil.process_iter():
        if p.name() == lcu_name:
            args = p.cmdline()

            for a in args:
                if '--region=' in a:
                    region = a.split('--region=', 1)[1].lower()
                if '--remoting-auth-token=' in a:
                    auth_token = a.split('--remoting-auth-token=', 1)[1]
                if '--app-port' in a:
                    app_port = a.split('--app-port=', 1)[1]
                if '--riotclient-auth-token=' in a:
                    riotclient_auth_token = a.split(
                        '--riotclient-auth-token=', 1)[1]
                if '--riotclient-app-port=' in a:
                    riotclient_app_port = a.split(
                        '--riotclient-app-port=', 1)[1]


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


connector = Connector()


@connector.ready
async def connect(connection):

    global showNotInChampSelect

    getLCUName()
    getLCUArguments()

    lcu_api = 'https://127.0.0.1:' + app_port
    riotclient_api = 'https://127.0.0.1:' + riotclient_app_port

    lcu_session_token = base64.b64encode(
        ('riot:' + auth_token).encode('ascii')).decode('ascii')

    riotclient_session_token = base64.b64encode(
        ('riot:' + riotclient_auth_token).encode('ascii')).decode('ascii')

    lcu_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Basic ' + lcu_session_token
    }

    riotclient_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'LeagueOfLegendsClient',
        'Authorization': 'Basic ' + riotclient_session_token
    }

    p_nb = 0
    try:
        checkForLobby = True
        while True:
            nameArr = []
            get_champ_select = lcu_api + '/lol-champ-select/v1/session'
            r = requests.get(get_champ_select,
                             headers=lcu_headers, verify=False)
            r = json.loads(r.text)
            if 'errorCode' in r:
                checkForLobby = True
                if showNotInChampSelect:
                    print('Not in champ select. Waiting for game...')
                    showNotInChampSelect = False
            else:
                if checkForLobby:
                    clear()
                    print('\n* Found lobby. *\n')
                    while 1:
                        try:
                            print("trying to get lobby")
                            get_lobby = riotclient_api + '/chat/v5/participants'
                            r = requests.get(
                                get_lobby, headers=riotclient_headers, verify=False)
                            r = json.loads(r.text)
                            # print("/chat/v5/participants")
                            # print(r)

                        except:
                            print("error getting lobby")
                        nameArr = []

                        p_nb += 1
                        # Issue found here.
                        #
                        # Sometimes the taken participant is more than 5.
                        # This causes making links and basic structure to fail.
                        # What causes this?
                        # This happens when the user/client is having a chat conversation with another player not in the lobby.
                        # This causes the chat/v5/participants to have more than 5 participants. (7 or more)
                        # This causes the program to fail.

                        # How to solve? (Temporary)
                        # Close conversations with other players.
                        # This will cause the chat/v5/participants to have 5 participants only.

                        # How to solve? (Permanent)
                        # We need to implement a CID (Conversation ID) checker.
                        # Due to how the chat/v5/participants works, it will always return the participants of the current conversation.
                        # may it be a conversation with a player in the lobby or in chat.
                        # We need to implement a CID checker to check if the conversation is in the lobby or not.
                        # A pattern found is that the CID of the lobby must have 5 participants.
                        # While CID of a conversation with a player is only 2. The chatter and the player.
                        # To olve this we need to find the CID of the lobby and then find the participants of that CID.
                        # If the participants of the CID is 5 then we can proceed to making links and basic structure.
                        # If the participants of the CID is less than 5 then we need to find the CID of the lobby again.
                        # This will loop until the CID of the lobby has 5 participants.

                        # Needs to be tested in Solo/Duo Rank environtment
                        # Sadly does not work in Co-op vs AI
                        #
                        # nameArr = []

                        # cid_counts = {}
                        # cid_with_5_counts = ''
                        # for participant in r['participants']:
                        #     cid = participant['cid']
                        #     if cid not in cid_counts:
                        #         cid_counts[cid] = 1
                        #     else:
                        #         cid_counts[cid] += 1

                        #     if cid_counts[cid] == 5:
                        #         cid_with_5_counts = cid
                        #         break

                        # if cid_with_5_counts == '':
                        #     # Find the CID with atleast more than 2 participants.
                        #     cid_with_5_counts = list(cid_counts.keys())[0]
                        #     for cid in cid_counts:
                        #         if cid_counts[cid] > 2:
                        #             cid_with_5_counts = cid
                        #             break

                        # for i in r:
                        #     if i['cid'] == cid_with_5_counts:
                        #         nameArr.append(i['game_name'] +
                        #                         "#" + i['game_tag'])

                        # Another possible solution but needs testing.
                        # From further testing champ-select lobbies have 'Riot' for 'activePlatform' while chat lobbies have 'None' for 'activePlatform'
                        # This can be used to filter out the participants of the lobby.
                        # This will cause the program to still work even if the user has a conversation with other players.

                        # for i in r['participants']:
                        #     if i['activePlatform'] is not 'None' and i['activePlatform'] is 'Riot':
                        #         nameArr.append(
                        #             i['game_name'] + "#" + i['game_tag'])

                        # This assumes that the user has no conversation with other players.
                        # This will cause the program to fail if the user has a conversation with other players.
                        # Unless the user has a conversation with other players in the lobby then it still works
                        # but if the user has a conversation with other players not in the lobby then it will fail.

                        for i in r['participants']:
                            nameArr.append(i['game_name'] +
                                           "#" + i['game_tag'])
                        print(nameArr)

                        if p_nb == 5:
                            print("found 5 players")
                            p_nb = 0
                            links = multi_search(nameArr)
                            print(links.opgg)
                            print(links.ugg)
                            # print(links.deeplolgg)
                            exit(0)

    except KeyboardInterrupt:
        print('\n\n* Exiting... *')
        sys.exit(0)


connector.start()
