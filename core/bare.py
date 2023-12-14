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
    # try:  # Needs to have a valid player puuid or summoner name or account id or username and tagline
    #     # watcher.summoner.by_name(my_region, 'KaiserV')
    #     watcher.summoner.by_name(my_region, 'Mikado')
    #     # watcher.summoner.by_puuid(my_region, 'afN65zfuFUsqAo_BbTYZIji8vl9ZgzSBoEgVnckAzgFIoSrxWpOZ2NxlZSD7cguUBlvNV8Ve9AFHfw')
    #     # watcher.summoner.by_puuid(my_region, '_KkxMDgbYyMEq3Whh2XhXSgBWmp1TSKosgXgsaBURB7-fI7EzEDeP0YjN8mako_RUY2zq_kBgyn5wA')

    # except ApiError:
    #     # open braves website
    #     print("your api key is not valid")
    #     exit(0)
    # print("your api key is valid")

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
                        for i in r['participants']:
                            nameArr.append(i['game_name'] +
                                           "#" + i['game_tag'])

                        if p_nb == 10:
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
