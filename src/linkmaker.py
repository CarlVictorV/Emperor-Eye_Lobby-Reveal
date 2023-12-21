import webbrowser

class multi_search:
    def __init__(self, nameArr):
        print("hi im multisearch: ", nameArr)
        self.nameArr = nameArr
        self.opgg()
        self.ugg()

    def open_link(self, link):
        webbrowser.open(link)

    def opgg(self):
        link = 'https://www.op.gg/multisearch/ph?summoners='
        link += ','.join(i.replace(' ', '+').replace(',', '%2C').replace('#', '%23') for i in self.nameArr)
        self.opgg = link

    def ugg(self):
        link = 'https://u.gg/multisearch?summoners='
        link += ','.join(i.replace(' ', '%20').replace('#', '-') for i in self.nameArr)
        link += '&region=ph2'
        self.ugg = link



class single_search:
    def __init__(self, data_container):
        print(data_container)
        self.nameArr = data_container
        self.opgg()
        self.ugg()
        self.tracker()
        self.leagueofgraphs()
        self.lolalytics()
        self.porogg()

    def open_link(self, link):
        webbrowser.open(link)

    def opgg(self):
        link = 'https://www.op.gg/summoners/ph/'
        for i in self.nameArr:
            link += i.replace(' ', '%2').replace('#', '-')
        self.opgg = link

    def ugg(self):

        link = 'https://u.gg/lol/profile/ph2/'
        for i in self.nameArr:
            link += i.replace(' ', '+').replace('#', '-')
        self.ugg = link

    def tracker(self):
        link = 'https://tracker.gg/lol/profile/riot/PH/'
        for i in self.nameArr:
            link += i.replace(' ', '%20').replace('#', '%23')
        self.tracker = link

    def leagueofgraphs(self):

        link = 'https://www.leagueofgraphs.com/summoner/ph/'
        for i in self.nameArr:
            
            link += i.replace(' ', '+').replace('#', '-')
        self.leagueofgraphs = link
        

    def lolalytics(self):

        link = 'https://xdx.gg/'
        for i in self.nameArr:
            link += i.replace(' ', '+').replace('#', '-')

        self.lolalytics = link
        

    def porogg(self):
        link = 'https://poro.gg/summoner/ph/'
        for i in self.nameArr:
            link += i.replace(' ', '%20').replace('#', '-')
        self.porogg = link
        print(link)

    def live_link(self, get_current_summoner):
        link = 'https://porofessor.gg/live/ph/'
        link += get_current_summoner.replace(' ', '+').replace('#', '%23')
        self.live_link = link

if __name__ == '__main__':
    multi_search()
    single_search()