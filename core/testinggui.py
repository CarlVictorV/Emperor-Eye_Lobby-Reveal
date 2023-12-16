import tkinter as tk
from tkinter import ttk
from lcu_driver import Connector
import requests
import json
import platform
import psutil
import base64
import sys
from os import system, name
import webbrowser

class multi_search:
    def __init__(self, nameArr):
        self.nameArr = nameArr
        self.opgg()
        self.ugg()

    def open_link(self, link):
        webbrowser.open(link)

    def opgg(self):
        link = 'https://www.op.gg/multisearch/ph?summoners='
        for i in self.nameArr:
            link += i.replace(' ', '+').replace(',', '%2C').replace('#', '%23')
            link += '%2C'
        self.opgg = link

    def ugg(self):
        link = 'https://u.gg/multisearch?summoners='
        for i in self.nameArr:
            link += i.replace(' ', '%20').replace('#', '-')
            link += ','
        link += '&region=ph2'
        self.ugg = link

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lobby Search App")
        self.root.geometry("500x400")

        # Create top layer
        self.top_frame = ttk.Frame(root, padding=(10, 10, 10, 10))
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Search button
        self.search_button = ttk.Button(self.top_frame, text="SEARCH", command=self.search)
        self.search_button.grid(row=0, column=0, padx=10, pady=10)

        # Option menu
        options = ["OP.GG", "U.GG", "Names Only"]
        self.option_var = tk.StringVar(self.top_frame)
        self.option_var.set(options[0])  # default value
        self.option_menu = ttk.Combobox(self.top_frame, textvariable=self.option_var, values=options, state='readonly')
        self.option_menu.grid(row=0, column=1, padx=10, pady=10)

        # Dodge button
        self.dodge_button = ttk.Button(self.top_frame, text="Dodge", command=self.dodge)
        self.dodge_button.grid(row=0, column=2, padx=10, pady=10)

        # Waiting label
        self.waiting_label = ttk.Label(root, text="Waiting for Lobby...")
        self.waiting_label.pack(pady=10)

        # Create players frame
        self.players_frame = ttk.Frame(root, padding=(10, 10, 10, 10))
        self.players_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create player buttons
        self.player_buttons = []
        for i in range(5):
            button = ttk.Button(self.players_frame, text=f"Player {i + 1}", command=lambda idx=i: self.open_link(idx))
            button.grid(row=i + 1, column=1, padx=10, pady=5)
            self.player_buttons.append(button)

        # Additional variables and setup for LCU connection
        self.lcu_name = None
        self.app_port = None
        self.auth_token = None
        self.riotclient_auth_token = None
        self.riotclient_app_port = None
        self.showNotInChampSelect = True

        self.connector = Connector()
        self.connector.start()
        
    def open_link(self, idx):
        if hasattr(self, 'links'):
            player_link = getattr(self.links, self.option_var.get().lower())
            webbrowser.open(player_link)

    def search(self):
        self.getLCUName()
        self.getLCUArguments()

        links = multi_search(nameArr)
        self.links = links

        lcu_api = 'https://127.0.0.1:' + self.app_port
        riotclient_api = 'https://127.0.0.1:' + self.riotclient_app_port

        lcu_session_token = base64.b64encode(
            ('riot:' + self.auth_token).encode('ascii')).decode('ascii')

        riotclient_session_token = base64.b64encode(
            ('riot:' + self.riotclient_auth_token).encode('ascii')).decode('ascii')

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
                    if self.showNotInChampSelect:
                        self.waiting_label.config(text="Not in champ select. Waiting for game...")
                        self.showNotInChampSelect = False
                else:
                    if checkForLobby:
                        self.waiting_label.config(text="\n* Found lobby. *")
                        while 1:
                            try:
                                get_lobby = riotclient_api + '/chat/v5/participants'
                                r = requests.get(
                                    get_lobby, headers=riotclient_headers, verify=False)
                                r = json.loads(r.text)
                            except:
                                pass
                            
                            nameArr = []
                            p_nb = 0

                            for i in r['participants']:
                                nameArr.append(i['game_name'] +
                                                "#" + i['game_tag'])
                                p_nb += 1

                            for i in range(5):
                                if i < p_nb:
                                    self.player_labels[i].config(text=nameArr[i])
                                else:
                                    self.player_labels[i].config(text=f"Player {i + 1}")

                            if p_nb == 5:
                                self.waiting_label.config(text="Found 5 players")
                                links = multi_search(nameArr)
                                print(links.opgg)
                                print(links.ugg)
                                # print(links.deeplolgg)
                                break
        except KeyboardInterrupt:
            print('\n\n* Exiting... *')

    def dodge(self):
        # Add functionality for the DODGE button
        pass

    def getLCUName(self):
        '''
        Get LeagueClient executable name depending on platform.
        '''
        if platform.system() == 'Windows':
            self.lcu_name = 'LeagueClientUx.exe'
        elif platform.system() == 'Darwin':
            self.lcu_name = 'LeagueClientUx'
        elif platform.system() == 'Linux':
            self.lcu_name = 'LeagueClientUx'

    def LCUAvailable(self):
        '''
        Check whether a client is available.
        '''
        return self.lcu_name in (p.name() for p in psutil.process_iter())

    def getLCUArguments(self):
        if not self.LCUAvailable():
            sys.exit('No ' + self.lcu_name + ' found. Login to an account and try again.')

        for p in psutil.process_iter():
            if p.name() == self.lcu_name:
                args = p.cmdline()

                for a in args:
                    if '--region=' in a:
                        self.region = a.split('--region=', 1)[1].lower()
                    if '--remoting-auth-token=' in a:
                        self.auth_token = a.split('--remoting-auth-token=', 1)[1]
                    if '--app-port' in a:
                        self.app_port = a.split('--app-port=', 1)[1]
                    if '--riotclient-auth-token=' in a:
                        self.riotclient_auth_token = a.split(
                            '--riotclient-auth-token=', 1)[1]
                    if '--riotclient-app-port=' in a:
                        self.riotclient_app_port = a.split(
                            '--riotclient-app-port=', 1)[1]

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()