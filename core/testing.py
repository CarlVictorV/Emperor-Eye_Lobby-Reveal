import sys
import requests
import json
import platform
import psutil
import base64
from os import system, name
from linkmaker import multi_search
from lcu_driver import Connector
from riotwatcher import LolWatcher, ApiError, RiotWatcher, Handlers
import warnings
warnings.filterwarnings('ignore')
# global variables

# Needs to be updated every 24 hours
api_key = 'RGAPI-3d89a098-93f3-40bf-b817-68cf2377da1b'
watcher = LolWatcher(api_key)
ratelim = Handlers.RateLimit.BasicRateLimiter()
deserializer = Handlers.DictionaryDeserializer()
account = RiotWatcher(api_key, 60, ratelim, deserializer)
my_region = 'ph2'
my_area = 'asia'

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

    get_lobby = riotclient_api + '/chat/v5/participants'
    r = requests.get(
        get_lobby, headers=riotclient_headers, verify=False)
    r = json.loads(r.text)
    print(r)

    # check = '/player-account/aliases/v1/display-name'
    # check = riotclient_api + check
    # r = requests.get(check, headers=riotclient_headers, verify=False)
    # r = json.loads(r.text)

    # if r == '':
    #     print("You are not logged in")
    #     exit(0)
    # else:
    #     current_gamename = r['gameName']
    #     current_tagline = r['tagLine']
    #     current_summoner = current_gamename + "#" + current_tagline
    #     print("You are logged in as " + current_summoner)

    # try:
    #     account_dto = account._account.by_riot_id(my_area, current_gamename, current_tagline)
    # except ApiError:
    #     print("your api key is not valid")
    #     exit(0)
    # print("your api key is valid")
    # print(account_dto)
    # get_summoner_details = watcher.summoner.by_puuid(my_region, account_dto['puuid'])
    # print(get_summoner_details)
    # get_ranked_stats = watcher.league.by_summoner(my_region, get_summoner_details['id'])
    # print(get_ranked_stats)

    # for j in get_ranked_stats:
    #     if j['queueType'] == 'RANKED_SOLO_5x5':
    #         print(j['tier'] + " " + j['rank'])
    #         print(j['leaguePoints'])
    #         print(j['wins'])
    #         print(j['losses'])
    #         print(j['veteran'])
    #         print(j['inactive'])
    #         print(j['freshBlood'])
    #         print(j['hotStreak'])

    # # ranked_stats = watcher.league.by_id


connector.start()
