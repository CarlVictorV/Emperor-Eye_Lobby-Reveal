import sys
import requests
import json
import platform
import psutil
import base64
from os import system, name
from linkmaker import multi_search, single_search
from lcu_driver import Connector
from riotwatcher import LolWatcher, ApiError, RiotWatcher, Handlers
import warnings
warnings.filterwarnings('ignore')
# global variables

# Needs to be updated every 24 hours
api_key = 'RGAPI-fc2bbfb7-2464-4968-bdb1-f29b0e031326'
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

    get_current_summoner = lcu_api + '/lol-summoner/v1/current-summoner'
    r = requests.get(get_current_summoner,
                     headers=lcu_headers, verify=False)
    r = json.loads(r.text)
    cur_gamename = r['gameName']
    cur_tagline = r['tagLine']
    cur_puuid = r['puuid']
    print(cur_gamename + "#" + cur_tagline)

    p_nb = 0
    p_c = 0
    r_f = False
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
                            print(r)

                        except:
                            print("error getting lobby")

                        nameArr = []
                        nameArrr = []
                        p_nb += 1

                        for i in r['participants']:
                            nameArrr.append(i['game_name'] + "#" + i['game_tag'])  # noqa
                            if i['activePlatform'] == 'riot':
                                nameArr.append(i['game_name'] + "#" + i['game_tag'])  # noqa
                                p_c += 1
                                r_f = True

                        if (p_nb >= 10 or p_c == 5) and r_f == True:
                            print("found 5 players")
                            p_nb = p_c = 0
                            print(nameArr)
                            links = multi_search(nameArr)
                            print(links.opgg)
                            print(links.ugg)
                            print("")
                            individual = single_search(nameArr)
                            individual.opgg()
                            print(individual.opgg)
                            try:
                                ranked_stats = []
                                for i in nameArr:
                                    temp_dto = account._account.by_riot_id(
                                        my_area, i.split("#")[0], i.split("#")[1])
                                    temp_summoner = watcher.summoner.by_puuid(
                                        my_region, temp_dto['puuid'])
                                    try:
                                        temp_ranked_stats = watcher.league.by_summoner(
                                            my_region, temp_summoner['id'])
                                    except KeyError:
                                        temp_ranked_stats = ['UNRANKED']
                                    ranked_stats.append(temp_ranked_stats)

                                for i in range(len(nameArr)):
                                    d = 0
                                    if ranked_stats[i] == ['UNRANKED'] or ranked_stats[i] == []:
                                        print(nameArr[i] + " is UNRANKED")
                                    else:
                                        for j in range(len(ranked_stats[i])):
                                            if ranked_stats[i][j]['queueType'] == 'RANKED_SOLO_5x5':
                                                print(
                                                    nameArr[i] + " is " + ranked_stats[i][j]['tier'] + " " + ranked_stats[i][j]['rank'] + " " + str(ranked_stats[i][j]['leaguePoints']) + "LP")
                                                print("Wins: " +
                                                      str(ranked_stats[i][j]['wins']) + " Losses: " + str(ranked_stats[i][j]['losses']))
                                                print("Winrate: " + str(
                                                    round(ranked_stats[i][j]['wins'] / (ranked_stats[i][j]['wins'] + ranked_stats[i][j]['losses']) * 100, 2)) + "%")
                                                d = 1
                                                break
                                        if d == 0:
                                            print(nameArr[i] + " is UNRANKED")
                                    print("")

                            except ApiError:
                                print("API Invalid")
                                print("Unable to utilize some features")

                            exit(0)
                        else:
                            p_c = 0
                            if r_f == True:
                                p_nb += 1

    except KeyboardInterrupt:
        print('\n\n* Exiting... *')
        sys.exit(0)


connector.start()
