import sys
import requests
import json
import platform
import psutil
import base64
from os import system, name
from lcu_driver import Connector
import warnings
from data import data_container
import asyncio
warnings.filterwarnings('ignore')

# global variables
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

def create_connector():
    return Connector()

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


def on_name_arr_updated(names):
    data_container.update_test(names)
    data = data_container.updated_test()
    print("i am now updated:", data)

connector = Connector()

@connector.ready
async def connect():
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
    
    get_current_summoner = lcu_api + '/lol-summoner/v1/current-summoner'
    r = requests.get(get_current_summoner,
                     headers=lcu_headers, verify=False)
    r = json.loads(r.text)
    cur_gamename = r['gameName']
    cur_tagline = r['tagLine']
    clear()
    print("WELCOME TO EMPEROR EYE")
    print("Current Summoner: ", cur_gamename + "#" + cur_tagline)
    

    foundRiotClient = False
    p_nb = 0
    try:
        checkForLobby = True
        while True:
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

                        except:
                            print("error getting lobby")

                        nameArr = []
                        for i in r['participants']:
                            if i['activePlatform'] == 'riot':
                                nameArr.append(i['game_name'] +
                                "#" + i['game_tag'])
                                foundRiotClient = True
                                p_nb += 1
                            
                        if (foundRiotClient and p_nb == 10) or (foundRiotClient and p_nb == 5):
                            print("Opening GUI...")
                            # Clean up the name array
                            # make sure names have no duplicates
                            nameArr = list(dict.fromkeys(nameArr))
                            
                            on_name_arr_updated(nameArr)    
                            return    

    except KeyboardInterrupt:
        print('\n\n* Exiting... *')
        sys.exit(0)


if __name__ == "__main__":
    asyncio.run(connect())